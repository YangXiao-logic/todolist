from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from todolist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'

login_manager.login_message_category = 'warning'
