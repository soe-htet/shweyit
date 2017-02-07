
from db import db
from models.authormodel import authormodel

class loginmodel(db.Model):
    __tablename__ = 'loginmodel'

    author_id = db.Column(db.Integer, primary_key = True)
    email= db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, author_id,email, password):
        self.author_id = author_id
        self.email = email
        self.password = password;

    def json(self):
        return {
                'author':authormodel.get_by_id(self.author_id)
                }

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(booktype=name).first()


    @classmethod
    def login(cls, email, password):
        return cls.query.filter((cls.email==email) & (cls.password==password)).first()

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
