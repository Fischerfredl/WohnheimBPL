import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!',
            'test': 'hih'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!',
            'test': 'dada'
        }
     ]
    return render_template('index.html', user=user, posts=posts)

@app.route('/Tabellen')
def tabellen():
    cur = g.db.execute("select SpielerID, Nickname, Vorname, Name from Spieler")
    spieler = [dict(ID=row[0], Nickname=row[1], Vorname=row[2], Nachname=row[3]) for row in cur.fetchall()]
    cur = g.db.execute("select TeamID, Name from Team")
    teams = [dict(ID=row[0], Name=row[1]) for row in cur.fetchall()]
    return render_template('tabellen.html', spieler=spieler, teams=teams)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', title='Login', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
