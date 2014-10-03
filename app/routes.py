from flask import Blueprint, render_template

from app.views import main

uber = Blueprint('uber', __name__, url_prefix='/uber',
                    template_folder='templates', static_folder='static')


@uber.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')

@uber.route("/")
def main_application():
    return main.google_maps()