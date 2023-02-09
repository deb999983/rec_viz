import os
from typing import Any
import django

from airflow.operators.python import PythonOperator, BranchPythonOperator


class DjangoOperatorMixin:
    def pre_execute(self, context: Any):
        super().pre_execute(context)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'operators.django.settings'
        django.setup(set_prefix=False)


class DjangoOperator(DjangoOperatorMixin, PythonOperator):
    pass


class BranchDjangoOperator(DjangoOperatorMixin, BranchPythonOperator):
    pass
