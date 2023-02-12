from rest_framework.generics import CreateAPIView, RetrieveAPIView
from applications.job.models import Job

from applications.job.serializers import JobSerializer


class ScheduleCodeRunJobView(CreateAPIView):
	serializer_class = JobSerializer
	queryset = Job.objects.all()


class JobDetailView(RetrieveAPIView):
	serializer_class = JobSerializer
	queryset = Job.objects.all()
	lookup_url_kwarg = 'code'
	lookup_field = 'code'