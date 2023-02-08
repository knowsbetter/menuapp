from celery.result import AsyncResult

from .main import app
from .menu_to_excel import convert_menu


@app.task
def to_excel(res):
    convert_menu(res)


@app.task
def get_status(task_id):
    return AsyncResult(task_id).status
