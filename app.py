from flask import Flask
from flask_pymongo import PyMongo
from model import mongo

# application setup
app = Flask(__name__)
app.config.from_object('config.Default')
app.config.from_pyfile('instance/config.cfg', silent=True)

# connect to db
mongo.init_app(app)

# initialize db
@app.before_first_request
def init_db():
    # create collections
    if 'users' not in mongo.db.collection_names():
        mongo.db.create_collection('users')
    if 'posts' not in mongo.db.collection_names():
        mongo.db.create_collection('posts')

    # add admin user if not exists
    admin = mongo.db.users.find_one({'username':'admin'})
    # password hash using sha256sum
    if admin is None:
        mongo.db.users.insert_one(dict(id=1, username='admin',
            password='8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'))

# registering blueprint
from admin import view as admin_page

app.register_blueprint(admin_page.page, url_prefix='/admin')

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)
