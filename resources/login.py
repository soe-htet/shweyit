import werkzeug
from flask_restful import Resource,reqparse
from models.loginmodel import loginmodel
from models.authormodel import authormodel


class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type= str, required= True, help= "This field is must!")
    parser.add_argument('password', type= str, required= True, help= "This field is must!")

    def get(self,username):
        tmp = loginmodel.get_by_name(username)
        if tmp:
            return tmp
        else:
            return {'message': 'login not found'}, 404

    def post(self):
        data = login.parser.parse_args()
        aut = loginmodel.login(data['email'],data['password'])

        if aut is None:
            return {'message':'login fail'},404
        else:
            return aut.json(),200


    def delete(self, name):
        if loginmodel.get_by_name(name) is None:
            return {'message','type doesn\'t exit'}, 404
        tmp = loginmodel.get_by_name(name)
        tmp.delete_from_db()
        return {'message','type deleted'}, 200



class register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type= str, required= True, help= "email is required!")
    parser.add_argument('password', type= str, required= True, help= "password is required!")
    parser.add_argument('author_name', type= str, required= True, help= "name is required!")
    parser.add_argument('author_nickname', type= str, required= True, help= "nickname is required!")

    def get(self,author_name):
        tmp = register.get_by_name(author_name)
        if tmp:
            return tmp
        else:
            return {'message': 'login not found'}, 404

    def post(self):
        data = register.parser.parse_args()
        reg = authormodel(data['email'],data['author_name'],data['author_nickname'])

        if authormodel.get_by_email(data['email']):
            return {'message': 'Email already exit'},404

        if authormodel.get_by_nickname(data['author_nickname']):
            return {'message': 'Nick Name already taken'},404

        try:
            reg.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        lgin = loginmodel(reg.id, reg.author_email, data['password'])
        try:
            lgin.save_to_db()
        except:
            return {'message': 'error occur second step logginable account'}, 500
        else:
            return reg.json(),200


