from celery import Celery

def make_celery(app_name=__name__):
    CELERY_BROKER_URL='amqp://localhost//'
    CELERY_RESULT_BACKEND='amqp://localhost//'
    
    
    return Celery(app_name, backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL, 
        CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml'], include=['myapp.tasks'])
   

celery=make_celery()


 

 