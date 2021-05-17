from flask import Flask
from mongoengine import connect
from flask_bcrypt import Bcrypt

from app.main.config import config_by_name

# You need to install mongodb locally

db = connect()

flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    global db
    print(config_by_name[config_name].DATABASE_URL)
    db = connect(alias=config_name,
                 host=config_by_name[config_name].DATABASE_URL)
    flask_bcrypt.init_app(app)

    return app
