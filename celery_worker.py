from myapp import celery
from myapp.factory import create_app
from myapp.celery_utils import init_celery

app=create_app()
init_celery(celery, app)