
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired,  Length, EqualTo, Regexp, ValidationError
from todolist.models import Category, User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='Username should only contain numbers and letters')])
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 128), EqualTo('password2')])

    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Name already in use.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 30)])
    content = StringField('TaskContent', validators=[DataRequired(), Length(1, 128)])
    deadline = SelectField('Deadline', coerce=int)
    category = SelectField('Category', coerce=int, default=1)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        # generate category and deadline select form choices
        super(TaskForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]
        self.deadline.choices =[i for i in range(1,30)]
