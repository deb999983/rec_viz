from django.urls import re_path
from .views import ScheduleCodeRunJobView

urlpatterns = [
    re_path(r'^$', ScheduleCodeRunJobView.as_view(), name='schedule_code_run_job_view'),
    # re_path(r'^jobs/(?P<code>\S{32}/$', views.ScheduleCodeRunJobView.as_view(), name='schedule_code_run_job_view')
]