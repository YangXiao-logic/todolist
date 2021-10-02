import os

from flask import Flask
from todolist.blueprints.home import home_bp
from todolist.blueprints.auth import auth_bp
from todolist.blueprints.todo import todo_bp
from todolist.extension import bootstrap, db, login_manager, moment

from todolist.setting import config

import click


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todolist')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_command(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todo_bp, url_prefix='/todo')


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--user', default=5, help='Quantity of categories, default is 10.')
    @click.option('--category', default=30, help='Quantity of posts, default is 50.')
    @click.option('--task', default=100, help='Quantity of comments, default is 500.')
    def forge(user, category, task):
        """Generate fake data."""
        from todolist.fakes import fake_tasks, fake_users, fake_categories

        db.drop_all()
        db.create_all()

        click.echo('Generating %d users...' % user)
        fake_users(user)

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d tasks' % task)
        fake_tasks(task)

        click.echo('Done.')
