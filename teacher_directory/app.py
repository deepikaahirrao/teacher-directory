import os
import yaml

from flask import Flask
from flask_restx import Api

from teacher_directory.models.config import Config


api = None
CONFIG = None


def load_config(config_file_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, "teacher_directory", config_file_name)
    with open(config_path) as fh:
        return Config(yaml.safe_load(fh.read()))


def init_api(app):
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }
    my_api = Api(
        app, doc='/', title="A teacher directory tool",
        description="A simple REST API for data processing",
        authorizations=authorizations)
    return my_api


def _init_db_client(app):
    from teacher_directory.db.collections import TeacherClient, UserClient
    client_map = {
        "teacher": TeacherClient,
        "user": UserClient
    }
    if "db" not in app.config:
        app.config["db"] = {}
    for key, client in client_map.items():
        if key not in app.config["db"]:
            app.config['db'][key] = client(app.config["database"].file_path)


def add_resources(my_api):
    from teacher_directory.resources.user import UserResource, LoginResource
    from teacher_directory.resources.teacher import (
        FeedDataResource, FilterResource, SearchResource, TeacherResource
    )
    my_api.add_resource(UserResource, "/user/")
    my_api.add_resource(LoginResource, "/login/")
    my_api.add_resource(TeacherResource, "/search-teacher/")
    my_api.add_resource(FeedDataResource, "/feed-data/")
    my_api.add_resource(FilterResource, "/teachers/")
    my_api.add_resource(SearchResource, "/teachers/<string:field>/<string:value>")


def create_app(config_filename="config.yaml"):
    """
    application factory method,Any configuration, registration, and
    other setup the application needs will happen inside the function
    :param config_filename: Configurations passed by config file
    :return: Flask instance
    """
    app = Flask(__name__)
    global CONFIG
    CONFIG = load_config(config_filename)
    app.config.update(CONFIG)

    global api
    api = init_api(app)

    from teacher_directory.db.connection import init_db
    init_db(app.config['database'])
    _init_db_client(app)

    add_resources(api)
    return app


