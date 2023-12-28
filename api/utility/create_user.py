from typing import Sequence

from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models as m
from app.logger import log

NUM_OF_FAKE_USERS = 30

faker = Faker()


def create_fake_users(db: Session, number_of_users: int = NUM_OF_FAKE_USERS):
    db_users: Sequence[str] = db.scalars(select(m.User.username)).all()
    counter = 0

    while counter < number_of_users:
        username = faker.name()
        if username in db_users:
            continue

        db_user = m.User(
            username=username,
            email=faker.email(),
            password=faker.password(),
        )
        db.add(db_user)
        counter += 1

    db.commit()
    log(log.INFO, f"Fake users ({counter}) created")
