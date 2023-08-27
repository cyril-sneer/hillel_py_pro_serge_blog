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


# Create your tasks here


from celery import shared_task
from django.core.mail import send_mail


@shared_task
def contact_us_email(*args, **kwargs):
    return send_mail(*args, **kwargs)
