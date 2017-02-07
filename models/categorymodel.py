
from db import db

class categorymodel(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key = True)
    category= db.Column(db.String)

    def __init__(self, category):
        self.category = category

    def json(self):
        return {
                'id': self.id,
                'category': self.category,
                }

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(category=name).first()

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
