from celery import Celery

# celery -A transport.main worker --loglevel=INFO --pool=solo
# celery -A transport.main flower

app = Celery("transport", broker="pyamqp://rabbitmq", backend="rpc://rabbitmq", include=["transport.tasks"])

if __name__ == "__main__":
    app.start()
