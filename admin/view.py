from flask import Blueprint
from flask import session, escape, redirect, url_for, render_template, request

from hashlib import sha256
from datetime import datetime

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

@page.route('/post', methods=['GET', 'POST'], endpoint='new_post')
def new_post():
    if not is_login():
        return render_template('login.html')
    if request.method == 'POST':
        judul = request.form.get('judul')
        isi   = request.form.get('isi')
        post = mongo.db.posts.insert_one(dict(judul=judul, isi=isi,
            author=session.get('username'), time=datetime.utcnow()))
        return render_template('content.html',
                content='Post baru berhasil ditambah: %s' %
                str(post.inserted_id))
    return render_template('new_post.html')
