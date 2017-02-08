import werkzeug
from flask_restful import Resource,reqparse
from models.categorymodel import categorymodel


class category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category', type= str, required= True, help= "This field is must!")

    def get(self,category):
        tmp = categorymodel.get_by_name(category)
        if tmp:
            return tmp
        else:
            return {'message', 'category not found'}, 404

    def post(self):
        data = category.parser.parse_args()
        if categorymodel.get_by_name(data['category']):
            return {'message':'category already exit'}, 400

        tmp = categorymodel(data['category'])
        try:
            tmp.save_to_db()
        except:
            return {'message': 'error occur while creating category'}, 500

        return tmp.json(), 201

    def delete(self, category):
        if categorymodel.get_by_name(category) is None:
            return {'message','category doesn\'t exit'}, 404
        tmp = categorymodel.get_by_name(category)
        tmp.delete_from_db()
        return {'message','category deleted'}, 200

class categorylist(Resource):
    def get(self):
        return {'categories': [x.json() for x in categorymodel.query.all()]}


