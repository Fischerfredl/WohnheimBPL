from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from functions import *


app_login = Blueprint('login', __name__, template_folder='templates')


@app_login.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if not validate_password(user, password):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            session['username'] = user
            flash('You were logged in: %s' % user)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app_login.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('home'))
