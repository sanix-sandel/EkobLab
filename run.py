from myapp import create_app
from myapp import make_celery

Myapp=create_app()
celery=make_celery(Myapp)


if __name__=='__main__':
    Myapp.run(debug=True)
    






