from flask import flash, redirect, url_for, render_template

from to_do_list import app, db
from to_do_list.forms import IsFinsihedForm, TaskForm
from to_do_list.models import Task

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = TaskForm()
#     if form.validate_on_submit():
#
#         title = form.title.data
#         body = form.body.data
#         task = Task(title=title, body=body)
#         db.session.add(task)
#         db.session.commit()
#         flash('Your task have been set!')
#         return redirect(url_for('index'))
#     tasks = Task.query.order_by(Task.timestamp.desc()).all()
#     return render_template('index.html', form=form, tasks=tasks)

# @app.route('/task/<int:task_id>/toggle', methods=['PATCH'])
# def toggle_task(task_id):
#     task=Task.query.get_or_404(task_id)
#     task.is_finished = not task.is_finished
#     return render_template('_task.html',task_id=task_id)
