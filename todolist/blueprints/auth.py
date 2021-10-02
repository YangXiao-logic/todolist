from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from todolist.forms import RegisterForm, LoginForm
from todolist.extension import db
from todolist.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user registered.', 'Success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user.validate_password(form.password.data):
            login_user(user, remember=True)

            redirect(url_for('todo.app'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logon')
def logon():
    return render_template('auth/logon.html')
