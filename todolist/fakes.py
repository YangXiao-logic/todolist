import random

from faker import Faker
from todolist.extension import db
from todolist.models import User, Category, Task

fake = Faker()


def fake_users(count=5):
    for i in range(count):
        user = User(username=fake.name(), password=fake.sentence())
        db.session.add(user)
    db.session.commit()


def fake_categories(count=30):
    for i in range(count):
        category = Category(
            name=fake.sentence(),
            user=User.query.get(random.randint(1, User.query.count()))
        )
        db.session.add(category)
    db.session.commit()


def fake_tasks(count=100):
    for i in range(count):
        category=Category.query.get(random.randint(1, Category.query.count()))
        task = Task(
            content=fake.sentence(),
            category=category,
            user=category.user
        )
        db.session.add(task)
    db.session.commit()
