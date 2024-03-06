from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, make_response
from flask_login import login_required, current_user, login_user, logout_user
from .forms import RegistrationForm
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Ensure the username and email are unique
        form.validate_username(form.username)
        form.validate_email(form.email)

        # Create a new user
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        login_user(new_user, remember=True)

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('views.home'))
    
    return render_template('sign_up.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        # Query the database for the user
        user = User.query.filter_by(username=username).first()
        
        # Check if the user exists and the password is correct
        if user:
            if user.check_password(password):
                flash('Logged in sucessfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print('Incorrect password')
                flash('Incorrect password, try again.', category='danger')
                return redirect(url_for('auth.login'))
        else:
            print('User does not exist')
            flash('Email does not exist.', category='danger')
            return redirect(url_for('auth.login'))


    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('auth.login'))

# Protected endpoint that requires flask-login - Testing purposes
@auth.route('/protected', methods=['GET'])
@login_required
def protected():
    return '<h1>Protected endpoint, youre authenticaded!</h1>'