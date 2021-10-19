from flask import flash, redirect, url_for, render_template, Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from todolist.forms import TaskForm
from todolist.extension import db
from todolist.models import Task, Category, User, Comment

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app', methods=['GET', 'POST'])
@login_required
def app():
    form = TaskForm()
    # Get the category of the current user
    form.category.choices = [(category.id, category.name)
                             for category in Category.query.with_parent(current_user).order_by(Category.name).all()]

    if form.validate_on_submit():
        # Create new task
        title = form.title.data
        content = form.content.data
        deadline = timedelta(days=form.deadline.data) + datetime.utcnow()
        category = Category.query.get(form.category.data)
        task = Task(title=title, content=content, category=category, user=current_user, deadline=deadline)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been set!')
        return redirect(url_for('todo.app'))
    # Get the tasks and count data from database.
    tasks = Task.query.with_parent(current_user).order_by(Task.timestamp.desc()).all()
    all_count = Task.query.with_parent(current_user).count()
    finished_count = Task.query.with_parent(current_user).filter_by(is_finished=True).count()
    unfinished_count = Task.query.with_parent(current_user).filter_by(is_finished=False).count()
    return render_template('todo/app.html', form=form, tasks=tasks, all_count=all_count, finished_count=finished_count,
                           unfinished_count=unfinished_count)


@todo_bp.route('/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def show_category(category_id):
    form = TaskForm()
    # Get the category of the current user
    form.category.choices = [(category.id, category.name)
                             for category in Category.query.with_parent(current_user).order_by(Category.name).all()]
    if form.validate_on_submit():
        # Create new task
        title =form.title.data
        content = form.content.data
        deadline=timedelta(days=form.deadline.data) + datetime.utcnow()
        category = Category.query.get(form.category.data)
        task = Task(title=title, content=content, category=category, user=current_user, deadline=deadline)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been set!')
        return redirect(url_for('todo.app'))
    # Get the tasks of current category and count data from database.
    current_category = Category.query.get_or_404(category_id)
    tasks = Task.query.with_parent(current_category).order_by(Task.timestamp.desc()).all()
    all_count = Task.query.with_parent(current_category).count()
    finished_count = Task.query.with_parent(current_category).filter_by(is_finished=True).count()
    unfinished_count = Task.query.with_parent(current_category).filter_by(is_finished=False).count()
    return render_template('todo/app.html', form=form, tasks=tasks, all_count=all_count, finished_count=finished_count,
                           unfinished_count=unfinished_count)

# Toggle the task
@todo_bp.route('/task/<int:task_id>/toggle', methods=['PATCH'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user != task.user:
        return jsonify(message='Permission denied')
    task.is_finished = not task.is_finished
    db.session.commit()
    return jsonify(message='task toggled')


# Delete the task
@todo_bp.route('/task/<int:task_id>/delete', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user != task.user:
        return jsonify(message='Permission denied')
    db.session.delete(task)
    db.session.commit()
    return jsonify(message='task deleted')

# Create the comment of the task.
@todo_bp.route('/comment/<int:task_id>/new', methods=['POST'])
@login_required
def new_comment(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    # Judge if the data is valid.
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid comment.'), 400
    comment = Comment(content=data['body'], task=task)
    db.session.add(comment)
    db.session.commit()
    return jsonify(html=render_template('todo/_comment.html', comment=comment))

# Create new category
@todo_bp.route('/category/new', methods=['POST'])
@login_required
def new_category():
    data = request.get_json()

    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid category.'), 400
    category = Category(name=data['body'], user=current_user)
    db.session.add(category)
    try:
        db.session.commit()
    except:
        flash('Category already exist')
        db.session.rollback()  # rollback if category is repeated.
    return jsonify(html=render_template('todo/_category.html', category=category), message='+1')
