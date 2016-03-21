import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from queries import *
from hashlib import sha1

# configuration
DATABASE = 'D:\\Dateien\\Dokumente\\GitHub\\WohnheimBPL\\database.db'
DEBUG = True
SECRET_KEY = 'development key'
ADMINLOGIN = 'admin'
ADMINPASS = 'admin'
MODLOGIN = 'mod'
MODPASSWORD = 'mod'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/comp')
def comp():
    table = query_db('SELECT WbID, Name FROM Wettbewerb')
    tablehead = ['WbID', 'Name']
    return render_template('comp.html', table=table, tablehead=tablehead)

@app.route('/comp/<int:compid>')
def compsite(compid):
    name = query_db('SELECT name FROM Wettbewerb WHERE WbID = ?', [compid], one=True)
    if not name:
        return render_template('notfound.html', entity='Wettbewerb')

    return render_template('detailcomp.html', name=name, compid=compid)

@app.route('/comp/<int:compid>/teams')
def compteams(compid):
    compname = query_db('SELECT name FROM Wettbewerb WHERE WbID = ?', [compid], one=True)
    if not compname:
        return render_template('notfound.html', entity='Wettbewerb')
    query = query_db('SELECT DISTINCT (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) AS teamn, \
                     (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = tg.SpielerID) AS spielern \
                     FROM Teilgenommen tg INNER JOIN Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                     WHERE uwb.WbID = ?', [compid])
    table = dict()
    for row in query:
        if row[0] not in table:
            table[row[0]] = []
        table[row[0]].append(row[1])

    return render_template('compteams.html', compname=compname, table=table)

@app.route('/comp/<int:leagueid>/<int:spieltag>')
def league(compid, leagueid):
    leaguename = query_db('SELECT name FROM Unterwettbewerb WHERE UnterwbID = ?', [leagueid], one=True)
    if not leaguename:
        return render_template('notfound.html', entity='Unterwettbewerb')
    return ('league.html', compid=compid, spieltag=spieltag)

@app.route('/team/<int:teamid>')
def teamsite(teamid):
    teamname = query_db('SELECT name FROM Team WHERE TeamID = ?', [teamid], one=True)
    if not teamname:
        return render_template('not_found.html' entity='Team')
    return render_template('detailteam.html', teamname=teamname)

@app.route('/player/<int:playerid>')
def playersite(playerid):
    playername = query_db('SELECT nickname FROM Spieler WHERE SpielerID = ?', [playerid], one=True)
    if not spielername:
        return render_template('not_found.html' entity='Spieler')
    return render_template('detailplayer.html', playername=playername)

@app.route('/game/<gameid>')
def gamesite(gameid):
    team1 = query_db('SELECT (SELECT name FROM Team WHERE Team.TeamID = Spiel.Team1ID) FROM Spiel WHERE SpielID = ?', [gameid], one=True)
    if not team1:
        return render_template('not_found.html' entity='Spiel')
    return render_template('detailgame.html')

@app.route('/login')
def login():
    return

@app.route('/logout')
def logout():
    return

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



if __name__ == '__main__':
    app.run()
