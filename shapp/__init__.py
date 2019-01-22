from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    with app.app_context():
        db.init_app(app)

    db.init_app(app)

    return app

app = create_app('default')

from .api import api
app.register_blueprint(api,url_prefix='/api')

