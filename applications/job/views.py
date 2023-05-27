import base64
import requests
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from applications.job.models import Job

from applications.job.serializers import JobSerializer


class ScheduleCodeRunJobView(CreateAPIView):
	auth_64 = base64.b64encode(b"airflow:airflow")

	serializer_class = JobSerializer
	queryset = Job.objects.all()

	def perform_create(self, serializer):
		job: Job = super().perform_create(serializer)
		resp = requests.post(
			"http://localhost:8080/api/v1/dags/process_job/dagRuns", 
			json={},
			headers={"Authorization": "Basic " + self.auth_64.decode()}
		)
		return job
  
	
class JobDetailView(RetrieveAPIView):
	serializer_class = JobSerializer
	queryset = Job.objects.all()
	lookup_url_kwarg = 'code'
	lookup_field = 'code'