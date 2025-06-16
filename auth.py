from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', category='success')
            # ✅ FIXED redirect: now goes to views.index
            return redirect(url_for('views.index'))
        else:
            flash('Invalid email or password.', category='error')

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('Passwords do not match.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=email, name=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', category='success')
            return redirect(url_for('auth.login'))  # ✅ stays the same

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.login'))
