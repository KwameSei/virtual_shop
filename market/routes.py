from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm() # Calling the register form
    if form.validate_on_submit():
        # Creating instance of a user
        user_create = User(
                            username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data
                          )
        # Submit the changes to the database
        db.session.add(user_create)
        db.session.commit()
        # Redirect user upon submission
        return redirect(url_for('market_page'))
        # Checking for errors
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'Error creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm() # Calling the login form
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):

            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username }', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Invalid email address or password! Please try again', category='danger')
    return render_template('login.html', form=form)