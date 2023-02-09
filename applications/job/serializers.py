import hashlib
from rest_framework import serializers
from django.db import transaction

from applications.job.models import Job, Code
from common import utils


class SourceCodeSerializer(serializers.Serializer):
    class Meta:
        model = Code
        fields = ('source', 'language', 'func_name',)


class JobSerializer(serializers.Serializer):
    source_code = SourceCodeSerializer()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'code', 'status', 'error',)
        
    def create(self, validated_data):
        source_code = validated_data['source']
        source_checksum = hashlib.md5(source_code).hexdigest()

        with transaction.atomic():
            code, _ = Code.objects.get_or_create(source_checksum=source_checksum, defaults=validated_data)
            job = Job.objects.create(source_code=code)
            utils.enqueue(job.id)
            
        return job
    