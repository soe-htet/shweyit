from flask import Flask,render_template
from flask_jwt import JWT
from flask_restful import Api
import os

from security import authenticate,identity

from resources.login import login,register
from resources.category import category
from resources.article import article,getarticles,getarticlesbycat

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "soe"
api = Api(app)
jwt = JWT(app, authenticate, identity)
app.config['UPLOAD_FOLDER'] = 'imgs/'


api.add_resource(register,'/register')
api.add_resource(login,'/login')
api.add_resource(category,'/add-category')
api.add_resource(article,'/post-article')
api.add_resource(getarticles,'/get-articles')
api.add_resource(getarticlesbycat,'/get-articles-cat')

@app.route('/')
def index():
    return render_template("hello.html")


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['pdf']
#       f2 = request.files['img']
#       filename = datetime.utcnow().strftime('%Y_%m_%d_%H%M%S%f')[:-3]
#       #tip = requests.post("http://burmesesoungs.com/mmnet/imgup.php",request.files['file'])
#       #tip  = urllib2.urlopen("http://burmesesoungs.com/mmnet/imgup.php",request.files['file'])
#       import requests
#       url = 'http://burmesesoungs.com/mmnet/imgup.php?filename='+filename
#       files = {'file': f2}
#       response = requests.post(url, files=files)
#       print(response.content)
#
#       url = 'http://burmesesoungs.com/mmnet/pdfup.php?filename='+filename
#       files = {'file': f}
#       response = requests.post(url, files=files)
#       print(response.content)
#
#       f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
#       return url_for('uploaded_file',
#                                 filename=f.filename)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001)

