from myapp import celery, create_app, init_celery

app=create_app()
app.app_context().push()