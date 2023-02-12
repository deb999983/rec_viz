import hashlib
import io
import json
from rest_framework.serializers import ModelSerializer
from django.db import transaction

from applications.job.models import Job, Code
from common import utils


class SourceCodeSerializer(ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'
        read_only_fields = ('id', 'source_checksum',)
    

class JobSerializer(ModelSerializer):
    source_code = SourceCodeSerializer()

    class Meta:
        model = Job
        fields = '__all__'        
        read_only_fields = ('id', 'code', 'status', 'source_filename', 'error', 'result',)
        
    def create(self, validated_data):
        source_code = validated_data['source_code']
        source_checksum = hashlib.md5(source_code['source'].encode('utf-8')).hexdigest()

        with transaction.atomic():
            code, _ = Code.objects.get_or_create(source_checksum=source_checksum, defaults=source_code)
            job = Job.objects.create(source_code=code)
            utils.enqueue(job.id)
            
        return job

    def to_representation(self, instance: Job):
        ret = super().to_representation(instance)
        if not instance.result:
            return ret

        ret['result'] = json.load(io.BytesIO(instance.result))
        return ret
