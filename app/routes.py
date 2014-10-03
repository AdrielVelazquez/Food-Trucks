from flask import Blueprint

partner = Blueprint('uber', __name__, url_prefix='/uber',
                    template_folder='templates', static_folder='static')