"""
CELERY WORKER MANAGE COMMAND:
celery -A lb_project worker -l INFO

# manage RabbitMQ
# stop the local node
sudo systemctl stop rabbitmq-server

# start it back
sudo systemctl start rabbitmq-server

# check on service status as observed by service manager
sudo systemctl status rabbitmq-server

# <-- run in Docker -->
docker run --name rabbit -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker container stop rabbit
docker container start rabbit
"""

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lb_project.settings')

app = Celery('lb_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')