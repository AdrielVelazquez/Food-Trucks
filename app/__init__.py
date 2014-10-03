from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import routes

from routes import uber

app.register_blueprint(uber)