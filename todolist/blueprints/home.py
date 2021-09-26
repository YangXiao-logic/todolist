from flask import render_template, flash, redirect, url_for, Blueprint

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return render_template('home/index.html')


@home_bp.route('/about')
def about():
    return render_template('home/about.html')
