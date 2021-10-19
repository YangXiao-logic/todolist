import random

from faker import Faker
from todolist.extension import db
from todolist.models import User, Category, Task, Comment

fake = Faker()


def fake_users(count=5):
    for i in range(count):
        user = User(username=fake.name())
        user.set_password('123456')
        db.session.add(user)
    db.session.commit()


def fake_categories(count=30):
    for i in range(count):
        category = Category(
            name=fake.word(),
            user=User.query.get(random.randint(1, User.query.count()))
        )
        db.session.add(category)
        try:
            db.session.commit()
        except:
            db.session.rollback()


def fake_tasks(count=100):
    for i in range(count):
        category = Category.query.get(random.randint(1, Category.query.count()))
        task = Task(
            title =fake.word(),
            content=fake.sentence(),
            category=category,
            user=category.user,
            deadline=fake.date_time_this_year(),
            timestamp=fake.date_time_this_year(),
            is_finished=random.choice([True, False])
        )
        db.session.add(task)
    db.session.commit()


def fake_comments(count=50):
    for i in range(count):
        task = Task.query.get(random.randint(1, Task.query.count()))
        comment = Comment(
            content=fake.sentence(),
            task=task
        )
        db.session.add(comment)
    db.session.commit()
