from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return render_template('../../../../../PycharmProjects/todolist/templates/auth/../templates/auth/login.html')


@auth_bp.route('/logon')
def logon():
    return render_template('../../../../../PycharmProjects/todolist/templates/auth/logon.html')
