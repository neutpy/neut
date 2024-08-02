from celery import Celery
from neut.core.settings import settings

celery_app = Celery("neut_tasks", broker=settings.CELERY_BROKER_URL)

celery_app.conf.update(task_track_started=True)

@celery_app.task
def example_task():
    return "Hello from Celery!"