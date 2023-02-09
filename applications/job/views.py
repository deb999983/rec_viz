from rest_framework.generics import CreateAPIView, RetrieveAPIView
from applications.job.models import Job

from applications.job.serializers import JobSerializer


class ScheduleCodeRunJobView(CreateAPIView):
	serializer_class = JobSerializer
	queryset = Job.objects.all()

	def perform_create(self, serializer):
		job = super().perform_create(serializer)
        
