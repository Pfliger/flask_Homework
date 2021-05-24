from datetime import datetime

from sqlalchemy import exc

import errors
from app import db


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck


class User(BaseModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))

    def to_dict(self):
        response = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        return response


class Post(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def to_dict(self):
        response = {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "created_date": self.created_date,
            "user": self.user_id
        }
        return response


