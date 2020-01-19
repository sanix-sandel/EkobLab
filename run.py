from myapp import create_app, celery


Myapp=create_app(celery=celery)


if __name__=='__main__':
    Myapp.run(debug=True)
    






