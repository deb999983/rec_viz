from datetime import datetime

from docker.types import Mount

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

from airflow.utils.db import provide_session
from airflow.models import XCom


from operators.django import DjangoOperator, DjangoSensor

def get_data_path_params(is_local=False):    
    if is_local:
        return Variable.get("local", deserialize_json=True)
    return Variable.get("prod", deserialize_json=True)
        

def wait_for_job(ti, **context):
    from common import utils
    job_id = utils.dequeue()
    if not job_id:
        return False            

    ti.xcom_push(key=f"wait_for_job.job_to_process", value=job_id)
    return True

def get_job_and_save_job_file(ti, job_key, **context):
    from applications.job.models import Job            
    job_id = ti.xcom_pull(key=job_key)
    
    try:
        path_params = get_data_path_params()
        source_path = f"{path_params['data_path']}/{path_params['code_path']}"
        
        job: Job = Job.prepare_for_run(job_id, source_path)
        return {
            "id": job.id, 
            "input_file_name": f'{job.source_filename}.{job.source_code.extension}',
            "output_file_name": f'{job.source_filename}.json',
            "func_name": job.source_code.func_name
        }
    except Exception as e:
        ti.xcom_push(key="error_info", value={"job_id": job_id})
        raise e

def save_result(ti, **context):
    from applications.job.models import Job
    
    job_info = ti.xcom_pull(task_ids='get_job_and_save_job_file', dag_id='process_job', key='return_value')
    try:
        path_params = get_data_path_params()
        output_path = f"{path_params['data_path']}/{path_params['output_path']}"
        
        exit_code = int(ti.xcom_pull(task_ids='run_job', dag_id='process_job', key='return_value'))
        Job.save_run_output(job_info['id'], output_path, exit_code)
    except Exception as e:
        ti.xcom_push(key="error_info", value={"job_id": job_info['id']})
        raise e        

def error_handler(ti, **context):
    from applications.job.models import Job
    error_info = ti.xcom_pull(dag_id='process_job', key='error_info')
    if not error_info:
        return
    
    job_id = error_info['job_id']
    Job.reset_status(job_id)
    
@provide_session
def cleanup_xcom(session=None, **context):
    dag_run = context["dag_run"]
    dag_run_id, dag_id = dag_run.run_id, dag_run.dag_id 
    session.query(XCom).filter(XCom.dag_id == dag_id, XCom.run_id == dag_run_id).delete()

with DAG(
    'process_job',
     description='This dag will be triggerd by through API', 
     schedule_interval=None,
     start_date=datetime(2022, 11, 18),
     catchup=False
) as dag:
    path_params = get_data_path_params()

    start = EmptyOperator(task_id="start")
    
    wait_for_a_job = DjangoSensor(task_id="wait_for_a_job", python_callable=wait_for_job)
    save_job_file = DjangoOperator(task_id="get_job_and_save_job_file", python_callable=get_job_and_save_job_file, op_kwargs={"job_key": "wait_for_job.job_to_process"})
    run_job = DockerOperator(
        task_id="run_job",
        image="deb999983/python_runner:1.0",
        command=[
            "src/executor.py",
            "{{ task_instance.xcom_pull(task_ids='get_job_and_save_job_file', dag_id='process_job', key='return_value') }}",
        ],
        environment={
            "CODE_PATH": f"{path_params.get('data_path')}/code/python",
            "OUTPUT_PATH": f"{path_params.get('data_path')}/output/python"
        },
        mem_limit=256 * 1024 * 1024,
        docker_url="tcp://docker-proxy:2375",
        mounts=[
            Mount(source=f"{path_params.get('data_path')}", target=f"{path_params.get('data_path')}", type="bind"),
        ],
        network_mode="bridge",
        auto_remove=True,
        force_pull=True,
        timeout=300
    )
    save_job_result = DjangoOperator(task_id="save_result", python_callable=save_result)
    
    handle_error = DjangoOperator(task_id="error_handler", python_callable=error_handler, trigger_rule="one_failed")
    
    cleanup = PythonOperator(task_id="cleanup_xcom", python_callable=cleanup_xcom, trigger_rule='none_failed')
    end = EmptyOperator(task_id='end', trigger_rule='none_failed')

    start >> wait_for_a_job >> save_job_file >> run_job >> save_job_result >> cleanup
    [save_job_file, save_job_result] >> handle_error >> cleanup
    cleanup >> end
    
    