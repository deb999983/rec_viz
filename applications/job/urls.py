from django.urls import re_path
from .views import ScheduleCodeRunJobView, JobDetailView

urlpatterns = [
    re_path(r'^$', ScheduleCodeRunJobView.as_view(), name='schedule_code_run_job_view'),
    re_path(r'^(?P<code>[a-z0-9A-Z_-]+)/$', JobDetailView.as_view(), name='schedule_code_run_job_view')
]