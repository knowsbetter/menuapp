from celery import Celery

from . import config

# celery -A transport.main worker --loglevel=INFO --pool=solo
# celery -A transport.main flower

app = Celery("transport", broker=config.RABBIT_BROKER, backend=config.RABBIT_BACKEND, include=["transport.tasks"])

if __name__ == "__main__":
    app.start()
