from flask import Blueprint, render_template, request

from app.views import main
from app.views import foodtrucks

uber = Blueprint('uber', __name__, url_prefix='/uber',
                    template_folder='templates', static_folder='static')


@uber.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')

@uber.route("/")
def main_application():
    return main.google_maps()

@uber.route("/open", methods=["GET"])
def food_trucks_open():
    #import pdb; pdb.set_trace()
    return foodtrucks.open()