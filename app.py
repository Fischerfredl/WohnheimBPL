import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from queries import *
from hashlib import sha1

# configuration
DATABASE = 'D:\\Dateien\\Dokumente\\GitHub\\WohnheimBPL\\database.db'
DEBUG = True
SECRET_KEY = 'development key'
# acc for administrator
ADMINLOGIN = 'admin'
ADMINPASSWORD = 'password'
# acc for tournament mods
MODLOGIN = 'mod'
MODPASSWORD = 'mod'

app = Flask(__name__)
app.config.from_object(__name__)

# routing

# Home: contains Blog for mods

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Navigation for comp-route:
# comp ->
# comp/compid->
# comp/compid/teams OR comp/leagueid/spieltag OR comp/groupid OR comp/koid

@app.route('/comp')
def comp():
    table = query_db('SELECT WbID, Name FROM Wettbewerb')
    return render_template('comp.html', table=table)

@app.route('/comp/<int:compid>')
def compdetail(compid):
    if not query_db('SELECT * FROM Wettbewerb WHERE WbID = ?', [compid], one=True):
        return error_handler('Wettbewerb nicht vorhanden')
    compname = query_db('SELECT Name FROM Wettbewerb WHERE WbID = ?', [compid], one=True)
    table_liga = query_db('SELECT uwb.UnterwbID, Name, MAX(Spieltag) \
                          FROM Unterwettbewerb uwb Inner Join \
                          (Spiel Inner Join Ligaspiel ON Spiel.SpielID = Ligaspiel.SpielID) AS sp \
                          ON uwb.UnterwbID = sp.UnterwbID \
                          WHERE  Modus = "liga" AND uwb.WbID = ? \
                          GROUP BY Name', [compid])
    table_turnier = query_db('SELECT UnterwbID, Name FROM Unterwettbewerb WHERE  Modus = "turnier" AND WbID = ?', [compid])
    table_ko = query_db('SELECT UnterwbID, Name FROM Unterwettbewerb WHERE  Modus = "ko" AND WbID = ?', [compid])

    return render_template('compdetail.html', compid=compid, compname=compname,

@app.route('/comp/<int:compid>/teams')
def compteams(compid):
    if not query_db('SELECT * FROM Wettbewerb WHERE WbID = ?', [compid], one=True):
        return error_handler('Wettbewerb nicht vorhanden')
    compname = query_db('SELECT Name FROM Wettbewerb WHERE WbID = ?', [compid], one=True)
    query = query_db('SELECT DISTINCT (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) AS teamn, \
                     (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = tg.SpielerID) AS spielern \
                     FROM Teilgenommen tg INNER JOIN Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                     WHERE uwb.WbID = ?', [compid])
    table = dict()
    for row in query:
        if row[0] not in table:
            table[row[0]] = []
        table[row[0]].append(row[1])
    return render_template('compteams.html', compid=compid, compname=compname, table=table)

# views for Unterwettbewerbe

@app.route('/comp/liga/<int:leagueid>/<int:spieltag>')
def league(leagueid, spieltag):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE UnterwbID = ?', [leagueid], one=True):
        return error_handler('Liga nicht vorhanden')
    max_spieltag = query_db('SELECT MAX(Spieltag) \
                            FROM  Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                            WHERE UnterwbID = ?', [leagueid], one=True)
    if spieltag<1 or spieltag >max_spieltag:
        return error_handler('Spieltag existiert nicht')
    leaguename = query_db('SELECT Name FROM Unterwettbewerb WHERE Modus = "liga" AND UnterwbID = ?', [leagueid], one=True)
    compid = query_db('SELECT WbID FROM Unterwettbewerb WHERE UnterwbID = ?', [leagueid], one=True)
    table_teamtabelle = getLigaTeamtabelle(leagueid, spieltag)
    table_spielertabelle = getSpielertabelle(leagueid, spieltag)
    table_spiele = getLigaSpiele(leagueid, spieltag)
    return render_template('league.html', leagueid=leagueid, leaguename=leaguename, compid=compid,
                           spieltag=spieltag, max_spieltag=max_spieltag,
                           table_teamtabelle=table_teamtabelle, table_spielertabelle=table_spielertabelle,
                           table_spiele=table_spiele)

@app.route('/comp/gruppe/<int:groupid>')
def group(groupid):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE Modus = "turnier" AND UnterwbID = ?', [groupid], one=True):
        return error_handler('Turniergruppe nicht vorhanden')
    groupname = query_db('SELECT Name FROM Unterwettbewerb WHERE UnterwbID = ?', [groupid], one=True)
    compid = query_db('SELECT WbID FROM Unterwettbewerb WHERE UnterwbID = ?', [groupid], one=True)
    table = query_db('SELECT SpielID FROM Spiel WHERE UnterwbID = ?', [groupid])
    return render_template('group.html', groupid=groupid, groupname = groupname, compid=compid, table=table)

@app.route('/comp/ko/<int:koid>')
def ko(koid):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE Modus = "ko" AND UnterwbID = ?', [koid], one=True):
        return error_handler('KO-Wettbewerb nicht vorhanden')
    koname = query_db('SELECT name FROM Unterwettbewerb WHERE UnterwbID = ?', [koid], one=True)
    compid = query_db('SELECT WbID FROM Unterwettbewerb WHERE UnterwbID = ?', [koid], one=True)
    table = query_db('SELECT SpielID FROM Spiel WHERE UnterwbID = ?', [koid])
    return render_template('ko.html', koid=koid, koname=koname, compid=compid, table=table)

# detail sites

@app.route('/team/<teamname>')
def detailteam(teamname):
    if not query_db('SELECT * FROM Team WHERE Name = ?', [teamname], one=True):
        return error_handler('Team nicht vorhanden')
    teamid = query_db('SELECT TeamID FROM Team WHERE Name = ?', [teamname], one=True)
    return render_template('detailteam.html', teamname=teamname, teamid=teamid)

@app.route('/player/<nickname>')
def detailplayer(nickname):
    if not query_db('SELECT * FROM Spieler WHERE Nickname = ?', [nickname]):
        return error_handler('Spieler gibbet nich')
    info = query_db('SELECT SpielerID, Nickname, Vorname, Name FROM Spieler WHERE Nickname = ?', [nickname])[0]
    return render_template('detailplayer.html', nickname=nickname, info=info)

@app.route('/game/<gameid>')
def detailgame(gameid):
    if not query_db('SELECT * FROM Spiel WHERE SpielID = ?', [gameid]):
        return error_handler('Spiel gibbet nich')
    return render_template('detailgame.html')

# login function

@app.route('/login')
def login():
    return

@app.route('/logout')
def logout():
    return

# custom functions
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0][0] if rv else None) if one else rv

# handle errors
def error_handler(error):
    return render_template('notfound.html', error=error)

# Database stuff
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

# app from console
if __name__ == '__main__':
    app.run()
