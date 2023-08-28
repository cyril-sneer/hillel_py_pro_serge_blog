# hillel_py_pro_serge_blog
Learning blog project + bootstrap styles 

# fixtures
learning_blogs_fixtures.dat

# available users
admin:admin
Sergey:qwe123QWE!@#

# CELERY WORKER MANAGE COMMAND:
celery -A lb_project worker -l INFO

# CELERY in Docker
docker run --name rabbit -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
