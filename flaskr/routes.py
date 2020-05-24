from flask import (
    Blueprint, g, redirect, render_template, url_for, flash, request, abort
)
from flaskr import db, bcrypt
import requests
from flaskr import app
from flaskr.models import User, TodoPost
from flaskr.forms import RegistrationForm, LoginForm, NewTodoForm, TodoForm
from flask_login import login_user, logout_user, login_required, current_user

# Setup a blueprint
bp = Blueprint('blog', __name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    todo_posts = TodoPost.query.all()
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if there are any emails with the same email the we've submitted
        user = User.query.filter_by(username=form.username.data).first()
        # If user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Hi there, {form.username.data}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Incorrect username or password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_todo_item():
    todo = NewTodoForm()
    if todo.validate_on_submit():
        todo_post = TodoPost(title=todo.title.data, content=todo.content.data, author=current_user)
        db.session.add(todo_post)
        db.session.commit()
        flash('Added New Item!', 'success')
        return redirect(url_for('index'))
    return render_template('create_todo_post.html', title="New Post", form=todo, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    todo_post = TodoPost.query.get_or_404(post_id)
    return render_template('todo_post.html', title=todo_post.title, post=todo_post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    todo_post = TodoPost.query.get_or_404(post_id)
    if todo_post.author != current_user:
        abort(403)
    form = TodoForm()
    if form.validate_on_submit():
        todo_post.title = form.title.data
        todo_post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=todo_post.id))
    elif request.method == 'GET':
        form.title.data = todo_post.title
        form.content.data = todo_post.content
    return render_template('create_todo_post.html', title=todo_post.title, form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    todo_post = TodoPost.query.get_or_404(post_id)
    if todo_post.author != current_user:
        abort(403)
    db.session.delete(todo_post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
