from rest_framework.generics import CreateAPIView, RetrieveAPIView
from applications.job.models import Job

from applications.job.serializers import JobSerializer


class ScheduleCodeRunJobView(CreateAPIView):
	serializer_class = JobSerializer
	queryset = Job.objects.all()
