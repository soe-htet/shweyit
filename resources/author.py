import werkzeug
from flask_restful import Resource,reqparse
from flask import url_for, make_response
from models.authormodel import authormodel

class author(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author_email', type= str, required= True, help= "This field is must!")
    parser.add_argument('author_name', type= str, required= True, help= "This field is must!")
    parser.add_argument('author_nickname', type= str, required= True, help= "This field is must!")


    def get(self,username):
        aut = authormodel.get_by_name(username)
        if aut:
            return aut
        else:
            return {'message', 'author not found'}, 404

    def post(self):
        data = author.parser.parse_args()
        if authormodel.get_by_email(data['author_email']):
            return {'message':'Email already exit'}, 400

        if authormodel.get_by_name(data['author_nickname']):
            return {'message':'Nick name already registered'}, 400

        aut = authormodel(data['username'],data['email'],data['password'])
        try:
            aut.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        return aut.json(), 201

    def delete(self, username):
        if authormodel.get_by_name(username) is None:
            return {'message','account doesn\'t exit'}, 404
        aut = authormodel.get_by_name(username)
        aut.delete_from_db()
        return {'message','account deleted'}, 200

class authorList(Resource):
    def get(self):
        return {'authors': [x.json() for x in authormodel.query.all()]}


class authorLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type= str, required= True, help= "email is required!")
    parser.add_argument('password', type= str, required= True, help= "password is required!")
    parser.add_argument('mobile',type=bool, required=False)
    def post(self):
        data = authorLogin.parser.parse_args()
        aut = authormodel.get_by_email(data['email'])
        tmppwd = bytes(data['password'], 'utf-8')
        if aut:
            if aut.password == data['password']:
                if data['mobile'] == None:
                    resp = make_response(url_for('upload_file1'))
                    resp.set_cookie('username', aut.username)
                    resp.set_cookie('id', str(aut.id))
                    return resp
                else:
                    return aut.json(), 200

            else:
                return {'message': 'incorrect email or password'},400

        return {'message': 'user not found'},404
