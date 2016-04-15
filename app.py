import os
import sqlite3
import platform
from flask import Flask, g, render_template
from contextlib import closing
from config import config_linux, config_windows
from competition.views import competition
from login.views import app_login
from user.views import user

app = Flask(__name__)


if platform.system() == 'Linux':
    app.config.from_object(config_linux)
elif platform.system() == 'Windows':
    app.config.from_object(config_windows)

app.register_blueprint(competition, url_prefix='/competition')
app.register_blueprint(app_login)
app.register_blueprint(user)

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
    return render_template('home.html')


# ----------------------------------------------------------------------------------------------------------------------
#
# admin view
#
# ----------------------------------------------------------------------------------------------------------------------

@app.route('/admin')
def admin():
    return 'Admin'


# allowed for option:
# newplayer, newteam, resetpw, delplayer, delteam
@app.route('/admin/settings/<option>', methods=['GET', 'POST'])
def adminsettings(option):
    return 'Admin settings: ' + option

# ----------------------------------------------------------------------------------------------------------------------
#
# settings
#
# ----------------------------------------------------------------------------------------------------------------------


# allowed for otion
# persona, password
@app.route('/user/<nickname>/settings/<option>', methods=['GET', 'POST'])
def playersettings(nickname, option):
    return 'Playersettings: ' + option + nickname


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
    app.run(host=app.config['IPADDR'], port=app.config['PORT'])
