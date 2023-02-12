import os
import uuid
from django.db import models, transaction
from common import utils

class Code(models.Model):
    class Status(models.TextChoices):
        PYTHON = "python"
        JAVASCRIPT = "js"
        TYPESCRIPT = "ts"

    extension_map = {
        Status.PYTHON: 'py',
        Status.JAVASCRIPT: 'js',
        Status.TYPESCRIPT: 'ts'
    }
    
    language = models.CharField(max_length=256, default="python")
    source = models.TextField(null=False)
    func_name = models.CharField(max_length=256)
    source_checksum = models.CharField(max_length=256, unique=True, null=False)

    @property
    def extension(self):
        return self.extension_map[self.language]
    

class Job(models.Model):
    class Status(models.IntegerChoices):
        QUEUED = 10
        RUNNING = 20
        COMPLETE = 30
        ERROR = 500
        
    code = models.UUIDField(unique=True, default = uuid.uuid4)
    status = models.IntegerField(choices=Status.choices, default=Status.QUEUED)

    source_code = models.ForeignKey(Code, on_delete=models.PROTECT)
    source_filename = models.CharField(max_length=256, null=False)

    error = models.TextField(null=True)
    result = models.JSONField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    def update_status(self, status):
        self.status = status
        self.save()
        
    def save_code_to_file(self, base_path: str):
        source_code: Code = self.source_code

        file_name = self.generate_filename()
        file = os.path.join(base_path, source_code.language, f'{file_name}.{source_code.extension}')
        with open(file, 'w') as fp:
            fp.write(source_code.source)

        self.source_filename = file_name
        self.save()
        
        print("Saved code to file", file) 
        return file_name

    def generate_filename(self):
        source_code: Code = self.source_code
        file_name = f'{self.code}_{source_code.func_name}_{self.created_on.timestamp()}'
        return file_name

    @classmethod
    def prepare_for_run(self, job_id: int, source_base_path: str):
        with transaction.atomic():
            try:
                job = Job.objects.select_related('source_code').filter(pk=job_id).select_for_update().first()            
                job.update_status(Job.Status.RUNNING)
                job.save_code_to_file(source_base_path)
                return job
            except Job.DoesNotExist as e:
                print(f'Job {job_id} doesnt exist')
                raise e
    
    @classmethod
    def save_run_output(self, job_id: int, output_file_path: str, exit_code: int):
        with transaction.atomic():
            job = Job.objects.select_related('source_code').filter(pk=job_id).select_for_update().first()

            source_code = job.source_code
            file = os.path.join(output_file_path, source_code.language, f'{job.source_filename}.json')
            with open(file) as fp:
                data = fp.read()
                if exit_code:
                    job.update_status(Job.Status.ERROR)
                    job.error = data
                else:
                    job.update_status(Job.Status.COMPLETE)
                    job.result = data
                job.save()
            return job

    @classmethod
    def reset_status(self, job_id: int):
        with transaction.atomic():
            job = Job.objects.filter(pk=job_id).select_for_update().first()
            job.update_status(Job.Status.QUEUED)
            job.save()
            utils.enqueue(job.id)
        return job
