
from db import db
from datetime import datetime
from models.categorymodel import categorymodel
from models.authormodel import authormodel

class articlemodel(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key = True)
    article_title= db.Column(db.String)
    article_detail= db.Column(db.String)
    article_image= db.Column(db.String)
    article_post_date= db.Column(db.DateTime)
    category_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)

    def __init__(self, title, detail, image, category_id, author_id):
        self.article_title = title
        self.article_detail = detail
        self.article_image = image
        self.article_post_date = datetime.now()
        self.category_id = category_id
        self.author_id = author_id

    def json(self):
        return {
                'id': self.id,
                'article_title': self.article_title,
                'article_detail': self.article_detail,
                'article_image': self.article_image,
                'article_post_date': self.article_post_date.strftime("%Y-%m-%d %H:%M:%S"),
                'category': categorymodel.get_by_id(self.category_id),
                'author': authormodel.get_by_id(self.author_id)
                }

    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter_by(article_title=title).first()

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

    @classmethod
    def getarticles(cls,page):
        articles = cls.query.order_by(cls.article_post_date.desc()).paginate(page=page, per_page=3)
        return articles

    @classmethod
    def getarticlesbycategory(cls,page,category_id):
        articles = cls.query.filter_by(category_id=category_id).paginate(page=page, per_page=2)
        return articles

    @classmethod
    def getarticlesbyauthor(cls,page,author_id):
        articles = cls.query.filter_by(author_id=author_id).paginate(page=page, per_page=2)
        return articles
