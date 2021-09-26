from flask import Flask
from todolist.blueprints.home import home_bp
from todolist.extension import bootstrap


def create_app():
    app = Flask('todolist')
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
