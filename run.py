from myapp import factory
import myapp 


if __name__=='__main__': 
    Myapp=factory.create_app(celery=myapp.celery)   
    Myapp.run(debug=True)





