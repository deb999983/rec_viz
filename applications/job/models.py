import uuid
from django.db import models


class Code(models.Model):
    class Status(models.TextChoices):
        PYTHON = "python"
        JAVASCRIPT = "js"
        TYPESCRIPT = "ts"

    language = models.CharField(default="python")
    source = models.TextField(null=False)
    func_name = models.CharField()
    source_checksum = models.CharField(unique=True, null=False)


class Job(models.Model):
    class Status(models.IntegerChoices):
        QUEUED = 10
        RUNNING = 20
        COMPLETE = 30
        ERROR = 500
        
    code = models.UUIDField(unique=True, default = uuid.uuid4)
    status = models.IntegerField(choices=Status.choices, default=Status.QUEUED)
    source_code = models.ForeignKey(Code, on_delete=models.PROTECT)
    source_file = models.CharField(max_length=256, null=False)
    error = models.TextField(null=True)
    result = models.JSONField(null=True)




