import os
import sqlite3
import platform
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from contextlib import closing
from config import config_linux, config_windows
from hashlib import sha1
from competition.views import competition
from login.views import login

app = Flask(__name__)


if platform.system() == 'Linux':
    app.config.from_object(config_linux)
elif platform.system() == 'Windows':
    app.config.from_object(config_windows)

app.register_blueprint(competition, url_prefix='/competition')
app.register_blueprint(login)

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
# Route: detail
#
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/team/<teamname>')
def detailteam(teamname):
    return ' Team: ' + teamname


@app.route('/player/<nickname>')
def detailplayer(nickname):
    return 'Player: ' + nickname


@app.route('/game/<int:gameid>')
def detailgame(gameid):
    return 'Game: ' + gameid


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
@app.route('/player/<nickname>/settings/<option>', methods=['GET', 'POST'])
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
