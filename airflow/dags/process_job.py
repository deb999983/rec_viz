import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.python import PythonSensor

from django.db import transaction

from common import utils

from ..operators.django import BranchDjangoOperator, DjangoOperator


def wait_for_job(ti, **context):
    job_id = utils.dequeue()
    if not job_id:
        return False            

    ti.xcom_push(key=f"wait_for_job.job_to_process", value=job_id)
    return True


def get_job(ti, job_key, **context):
    from applications.job.models import Job
    job_id = ti.xcom_pull(key=job_key)
    
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist as e:
        print(f'Job {job_id} doesnt exist')
        raise e
    
    return job

def save_code(ti, job, **context):
    pass
        
    


def setup_container(ti, tg, **context):
    pass


with DAG(
    'process_job',
     description='This dag will be triggerd by through API', 
     schedule_interval=None,
     start_date=datetime(2022, 11, 18),
     catchup=False
):
    start = EmptyOperator(task_id="start")
    wait_for_job = PythonSensor()

    cleanup = PythonOperator(task_id="cleanup_xcom", python_callable=cleanup_xcom)
    end = EmptyOperator(task_id='end', trigger_rule='none_failed')

    start >> check_link_and_mark_to_process >> api_crawler_tg >> cleanup >> end
    check_link_and_mark_to_process >> end