from flask import Blueprint
from flask import session, escape, redirect, url_for, render_template, request
from flask import abort

from functools import wraps
from hashlib import sha256

from model import mongo

page = Blueprint('admin_page', __name__, 
        template_folder='templates')

def is_login():
    return 'username' in session

@page.route('/', endpoint='index')
def index():
    if not is_login():
        return render_template('login.html')
    return render_template('content.html', content='Admin landing page')

@page.route('/login', methods=['POST'], endpoint='login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = mongo.db.users.find_one(dict(username=username))
    pwd = sha256(password.encode('utf-8')).hexdigest()
    if user and pwd == user.get('password'):
        session['username'] = username
        return redirect(url_for('.index'))
    return 'login failed'

@page.route('/logout', endpoint='logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('.index'))
