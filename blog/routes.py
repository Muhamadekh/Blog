import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from blog import app, db, bcrypt
from blog.models import User, Post
from blog.forms import RegistrationForm, LoginForm, AccountForm
from flask_login import login_user, logout_user, login_required, current_user



posts = [
    {'title': 'Blog Post 1',
     'author': 'Moha',
     'date_posted': '21-April-2020',
     'content': 'First Blog Content'
     },
    {'title': 'Blog Post 2',
    'author': 'Haji',
    'date_posted': '21-April-2021',
    'content': 'Second Blog Content'
         }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home Page', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'An account has been created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Successful login", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check your details')
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = AccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your info has been changed ')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form, image_file=image_file)
