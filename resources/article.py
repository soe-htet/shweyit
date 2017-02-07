import werkzeug
from flask_restful import Resource,reqparse
from models.articlemodel import articlemodel
from flask import request,jsonify


class article(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('article_title', type= str, required= True, help= "Title is required!")
    parser.add_argument('article_detail', type= str, required= True, help= "Detail is required!")
    parser.add_argument('article_image', type= str, required= True, help= "Image link is required!")
    parser.add_argument('category_id', type= int, required= True, help= "Category id is required!")
    parser.add_argument('author_id', type= int, required= True, help= "Author id is required!")

    def get(self,id):
        tmp = articlemodel.get_by_id(id)
        if tmp:
            return tmp
        else:
            return {'message', 'article not found'}, 404

    def post(self):
        data = article.parser.parse_args()
        if articlemodel.get_by_title(data['article_title']):
            return {'message':'Already already exit'}, 400

        tmp = articlemodel(data['article_title'],data['article_detail'],data['article_image'],data['category_id'],data['author_id'])
        try:
            tmp.save_to_db()
        except:
            return {'message': 'error occur while creating article'}, 500

        return tmp.json(), 201

    def delete(self, name):
        if articlemodel.get_by_title(name) is None:
            return {'message','article doesn\'t exit'}, 404
        tmp = articlemodel.get_by_title(name)
        tmp.delete_from_db()
        return {'message','article deleted'}, 200


class getarticles(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type= int)

    def get(self):
        data = getarticles.parser.parse_args()
        pg_id = 1;
        if data["id"] is not None:
            pg_id = data["id"]
        articles = articlemodel.getarticles(pg_id)
        next_c = pg_id + 1;
        article_items = articles.items
        article_next = "null"
        print(articles.has_next)
        if articles.has_next:
            article_next = request.base_url + "?id=" + str(next_c)

        return jsonify(results=[i.json() for i in article_items],next=article_next)


class getarticlesbycat(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type= int)
    parser.add_argument('category_id', type= int)

    def get(self):
        data = getarticlesbycat.parser.parse_args()
        pg_id = 1;
        cat_id = 0;
        if data["id"] is not None:
            pg_id = data["id"]
        if data["category_id"] is None:
            return {"message": "category id not specified"},404
        cat_id = data["category_id"]
        articles = articlemodel.getarticlesbycategory(pg_id,cat_id)
        next_c = pg_id + 1;
        article_items = articles.items
        article_next = "null"
        print(articles.has_next)
        if articles.has_next:
            article_next = request.base_url + "?id=" + str(next_c) + "&category_id=" + str(cat_id)

        return jsonify(results=[i.json() for i in article_items],next=article_next)


class getarticlesbyauth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type= int)
    parser.add_argument('author_id', type= int)

    def get(self):
        data = getarticles.parser.parse_args()
        pg_id = 1;
        if data["id"] is not None:
            pg_id = data["id"]
        if data["author_id"] is None:
            return {"message": "author id not specified"},404
        articles = articlemodel.getarticlesbyauthor(pg_id,data["author_id"])
        next_c = pg_id + 1;
        article_items = articles.items
        article_next = "null"
        print(articles.has_next)
        if articles.has_next:
            article_next = request.base_url + "?id=" + str(next_c) + "&author_id=" + data["author_id"]

        return jsonify(results=[i.json() for i in article_items],next=article_next)


