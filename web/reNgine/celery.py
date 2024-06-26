import os
from celery import Celery
from celery.signals import after_setup_task_logger
from celery.app.log import TaskFormatter
from django.conf import settings
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reNgine.settings')

app = Celery('reNgine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(TaskFormatter('[%(asctime)s %(task_id)s %(filename)s:%(lineno)d] %(levelname)s - %(message)s'))

    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)