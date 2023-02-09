from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^jobs/$', views.ScheduleCodeRunJobView.as_view(), name='schedule_code_run_job_view'),
    # re_path(r'^jobs/(?P<code>\S{32}/$', views.ScheduleCodeRunJobView.as_view(), name='schedule_code_run_job_view')
]