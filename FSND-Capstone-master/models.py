from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
import os

database_path = os.environ["DATABASE_URL"]
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def rollback():
    db.session.rollback()


class Movie(db.Model):
    __tablename__ = "public.actors"
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    release_date = Column(DateTime, nullable=False)

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
            }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = "public.actors"
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
