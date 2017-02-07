
from db import db
import base64

class authormodel(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key = True)
    author_email = db.Column(db.String(80))
    author_name = db.Column(db.String(80))
    author_nickname = db.Column(db.String(80))
    confirmed = db.Column(db.Boolean)

    def __init__(self,email, name, nickname):
        self.author_email = email
        self.author_name = name
        self.author_nickname = nickname
        self.confirmed = False

    def json(self):
        return {
                'id': self.id,
                'author_email': self.author_email,
                'author_name': self.author_name,
                'author_nickname': self.author_nickname,
                'confirmed': self.confirmed,
                }

    @classmethod
    def get_by_nickname(cls, nickname):
        return cls.query.filter_by(author_nickname=nickname).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(author_email=email).first()

    @classmethod
    def get_by_id(cls, id):
        model = cls.query.filter_by(id=id).first()
        if model:
            return model.json()
        return {'user':'null'}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
