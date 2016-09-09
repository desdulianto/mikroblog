from flask import Flask
from flask_pymongo import PyMongo

# application setup
app = Flask(__name__)
app.config.from_object('config.Default')
app.config.from_pyfile('config.cfg', silent=True)

# connect to db
mongo = PyMongo(app)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)
