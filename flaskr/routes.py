from flask import (
    Blueprint, g, redirect, render_template, request, url_for, flash
)
from flaskr import db
import requests
from werkzeug.exceptions import abort
from flaskr import app
from flaskr.models import User, TodoPost
from flaskr.forms import RegistrationForm, LoginForm

# Setup a blueprint
bp = Blueprint('blog', __name__)

@app.route('/')
def index():
    todo_posts = TodoPost.query.filter().all()
    # Api weather call
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=4af6fc5e2329133614788c5eb616f87d'
    city = 'Las Vegas' # Las Vegas
    response = requests.get(url.format(city)).json()
    weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon' : response['weather'][0]['icon'],
    }
    return render_template('/index.html', posts=todo_posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('register.html', title='Login', form=form)