from os import environ
import sqlite3
import platform
from flask import Flask, g, render_template, redirect, url_for, session
from contextlib import closing
from config import config_linux, config_windows
from functions_general import query_db
from competition.views import competition
from login.views import app_login
from user.views import user
from settings.views import settings
from table_views.views import table_views

app = Flask(__name__)


if platform.system() == 'Linux':
    app.config.from_object(config_linux)
elif platform.system() == 'Windows':
    app.config.from_object(config_windows)

app.register_blueprint(competition, url_prefix='/competition')
app.register_blueprint(app_login)
app.register_blueprint(user)
app.register_blueprint(settings, url_prefix='/settings')
app.register_blueprint(table_views)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#
# Views
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/')
@app.route('/home')
def home():
    return redirect(url_for('competition.overview'))

@app.route('/about')
def about():
    return render_template('about.html', page_title='About')


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#
# Database stuff
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


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
    nav = dict()
    for row in query_db("SELECT WbID, UnterwbID FROM Unterwettbewerb"):
        if row[0] not in nav:
            nav[row[0]] = []
        nav[row[0]].append(row[1])
    nav_compinfo = dict()
    for row in query_db("SELECT WbID, Name, Phase FROM Wettbewerb"):
        nav_compinfo[row[0]] = [row[1], row[2]]
    nav_divinfo = dict()
    for row in query_db("SELECT UnterwbID, Name, Modus FROM Unterwettbewerb"):
        nav_divinfo[row[0]] = [row[1], row[2]]

    session['nav'] = nav
    session['nav_compinfo'] = nav_compinfo
    session['nav_divinfo'] = nav_divinfo


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#
# Running app from console
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
