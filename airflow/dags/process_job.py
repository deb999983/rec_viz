from datetime import datetime
import os

from docker.types import Mount

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.sensors.python import PythonSensor
from airflow.providers.docker.operators.docker import DockerOperator

from django.db import transaction


from operators.django import DjangoOperator, DjangoSensor

def get_data_path_params(is_local=False):    
    if is_local:
        return Variable.get("local", deserialize_json=True)
    return Variable.get("prod", deserialize_json=True)
        

def wait_for_job(ti, **context):
    # from common import utils
    # job_id = utils.dequeue()
    # if not job_id:
    #     return False            
    from applications.job.models import Job
    job = Job.objects.filter(status=Job.Status.QUEUED).first()
    if not job:
        return False

    ti.xcom_push(key=f"wait_for_job.job_to_process", value=job.id)
    return True

def get_job_and_save_job_file(ti, job_key, **context):
    from applications.job.models import Job, Code
    
    def save_code_to_file(job: Job, base_path):
        code: Code = job.source_code
        file_name = f'{job.code}_{code.func_name}_{job.created_on.timestamp()}.py'
        file = os.path.join(base_path, code.language, file_name)
        
        with open(file, 'w') as fp:
            fp.write(code.source)
        return file
            
    job_id = ti.xcom_pull(key=job_key)
    
    try:
        job = Job.objects.get(pk=job_id)

        path_params = get_data_path_params()
        file = save_code_to_file(job, f"{path_params['data_path']}/{path_params['code_path']}")
        
        job.source_file = file
        job.save()
        
        print("Saved code to file", file)
        return {
            "id": job.id, 
            "file": job.source_file, 
            "file_name": os.path.basename(job.source_file),
            "func_name": job.source_code.func_name
        }
    except Job.DoesNotExist as e:
        print(f'Job {job_id} doesnt exist')
        raise e


def save_result(ti, job_info, **context):
    from applications.job.models import Job, Code    
    try:
        job = Job.objects.get(pk=job_info['id'])

        path_params = get_data_path_params()
        output_path = f"{path_params['data_path']}/{path_params['output_path']}"
        file = os.path.join(output_path, "python", job_info['file_name'])
        
        with open(file, 'r') as fp:
            job.result = fp.read()
            job.save()
        
    except Job.DoesNotExist as e:
        print(f"Job {job_info['id']} doesnt exist")
        raise e


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
            "CODE_PATH": '/data/code/python',
            "OUTPUT_PATH": '/data/output/python'
        },
        docker_url="tcp://docker-proxy:2375",
        mounts=[
            Mount(source=f"{path_params.get('data_path')}", target="/data", type="bind"),
        ],
        network_mode="bridge"
    )
    save_job_result = DjangoOperator(task_id="save_result", python_callable=save_result, op_kwargs={"job_info": save_job_file.output})
    
    end = EmptyOperator(task_id='end', trigger_rule='none_failed')

    wait_for_a_job >> save_job_file >> run_job >> save_job_result >> end