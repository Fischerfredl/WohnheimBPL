import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from queries import *

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
@app.route('/index')
def index():
    cur = g.db.execute("select uwb.UnterwbID, Wettbewerb.Name, uwb.Name, uwb.Start, uwb.Ende FROM Unterwettbewerb uwb INNER JOIN Wettbewerb ON uwb.WbID = Wettbewerb.WbID WHERE uwb.modus = 'liga'")
    table = [dict(id=row[0], wbname=row[1], unterwb=row[2], start=row[3], ende=row[4]) for row in cur.fetchall()]
    return render_template('tabellen.html', title='Wettbewerbe', table=table)

@app.route('/Spieler')
def spieler():
    return render_template('tabellen.html', table=getSpieler(), title='Spieler')

@app.route('/Teams')
def teams():
    return render_template('tabellen.html', table=getTeams(), title='Teams')

@app.route('/<int:unterwb>/<int:spieltag>')
def teamtabelle(unterwb, spieltag):
    max_spieltag = g.db.execute("SELECT MAX(ls.Spieltag) FROM Ligaspiel ls INNER JOIN Spiel s ON s.SPielID = ls.SpielID WHERE s.UnterwbID = ?", [unterwb]).fetchall()[0][0]
    return render_template('tabellen.html', title='Teamtabelle', max_spieltag=max_spieltag, table_st=getSpieltag(unterwb, spieltag), table_t=getTeamtabelle(unterwb, spieltag), spieler_t=getSpielertabelle(unterwb, spieltag), unterwb=unterwb, spieltag=spieltag)

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

@app.route('/anlegen', methods=['GET', 'POST'])
def anlegen():
    error = None
    if request.method =='POST':
        if request.form['username'] not in g.db.execute("SELECT Spieler FROM Spieler").fetchall():
            error = 'Invalid username'

    return render_template('anlegen.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
