from flask import Blueprint, render_template

uber = Blueprint('uber', __name__, url_prefix='/uber',
                    template_folder='templates', static_folder='static')


@uber.route("/")
def main_application():
    return render_template("index.html")