from .main import app
from .menu_to_excel import convert_menu


@app.task
def to_excel(res):
    convert_menu(res)
