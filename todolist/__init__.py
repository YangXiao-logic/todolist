import os

from flask import Flask, render_template
from flask_login import current_user

from todolist.blueprints.home import home_bp
from todolist.blueprints.auth import auth_bp
from todolist.blueprints.todo import todo_bp
from todolist.extension import bootstrap, db, login_manager, moment, csrf, migrate
from todolist.models import Category
from todolist.setting import config

import click


def create_app(config_name=None):
    # default setting
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todolist')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_command(app)
    register_template_context(app)

    return app

# register extensions
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

# register blueprints
def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todo_bp, url_prefix='/todo')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        # categories for app and category page
        if current_user.is_authenticated:
            categories = Category.query.with_parent(current_user).order_by(Category.name).all()
        else:
            categories = None
        return dict(categories=categories)


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
    @click.option('--user', default=5, help='Quantity of categories, default is 5.')
    @click.option('--category', default=30, help='Quantity of posts, default is 30.')
    @click.option('--task', default=100, help='Quantity of comments, default is 100.')
    @click.option('--comment', default=50, help='Quantity of comments, default is 50.')
    def forge(user, category, task, comment):
        """Generate fake data."""
        from todolist.fakes import fake_tasks, fake_users, fake_categories, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating %d users...' % user)
        fake_users(user)

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d tasks' % task)
        fake_tasks(task)

        click.echo('Generating %d tasks' % comment)
        fake_comments(comment)
        click.echo('Done.')
