from flask import flash, redirect, url_for, render_template, Blueprint
from flask_login import login_required, current_user
from todolist.forms import TaskForm
from todolist.extension import db
from todolist.models import Task, Category, User

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app', methods=['GET', 'POST'])
def app():
    form = TaskForm()
    form.category.choices=[(category.id, category.name)
     for category in Category.query.with_parent(current_user).order_by(Category.name).all()]
    if form.validate_on_submit():
        content = form.content.data
        category = Category.query.get(form.category.data)
        task = Task(content=content, category=category, user=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been set!')
        return redirect(url_for('app'))
    categories = Category.query.with_parent(current_user).order_by(Category.timestamp.desc()).all()
    all_tasks = Task.query.with_parent(current_user).order_by(Task.timestamp.desc()).all()
    finished_tasks = Task.query.with_parent(current_user).filter_by(is_finished=True).order_by(Task.timestamp.desc()).all()
    unfinished_tasks = Task.query.with_parent(current_user).filter_by(is_finished=False).order_by(Task.timestamp.desc()).all()
    return render_template('todo/app.html', all_tasks=all_tasks, finished_tasks= finished_tasks, unfinished_tasks= unfinished_tasks, categories=categories, form=form)



@todo_bp.route('/category/<int:category_id>')
def show_category(category_id):
    current_category = Category.query.get_or_404(category_id)
    tasks = Task.query.with_parent(current_category).order_by(Task.timestamp.desc().all())
    return render_template('todo/category.html')

# @todo_bp.route('/app', methods=['GET', 'POST'])
# def index():
# form = TaskForm()
# if form.validate_on_submit():
#
#     title = form.title.data
#     body = form.body.data
#     task = Task(title=title, body=body)
#     db.session.add(task)
#     db.session.commit()
#     flash('Your task have been set!')
#     return redirect(url_for('index'))
# tasks = Task.query.order_by(Task.timestamp.desc()).all()
# return render_template('index.html', form=form, tasks=tasks)

# @todo_bp.route('/task/<int:task_id>/toggle', methods=['PATCH'])
# def toggle_task(task_id):
#     task=Task.query.get_or_404(task_id)
#     task.is_finished = not task.is_finished
#     return render_template('_task.html',task_id=task_id)
