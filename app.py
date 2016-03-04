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
    cur = g.db.execute("select uwb.UnterwbID, Wettbewerb.Name, uwb.Name, uwb.Start, uwb.Ende FROM Unterwettbewerb uwb INNER JOIN Wettbewerb ON uwb.WbID = Wettbewerb.WbID WHERE uwb.modus = 'liga'")
    table = [dict(id=row[0], wbname=row[1], unterwb=row[2], start=row[3], ende=row[4]) for row in cur.fetchall()]
    return render_template('tabellen.html', title='Wettbewerbe', table=table)

@app.route('/Spieler')
def spieler():
    cur = g.db.execute("select SpielerID, Nickname, Vorname, Name from Spieler")
    spieler = [dict(ID=row[0], Nickname=row[1], Vorname=row[2], Nachname=row[3]) for row in cur.fetchall()]
    return render_template('tabellen.html', table=spieler, title='Spieler')

@app.route('/Teams')
def teams():
    cur = g.db.execute("select TeamID, Name from Team")
    teams = [dict(ID=row[0], Name=row[1]) for row in cur.fetchall()]
    return render_template('tabellen.html', table=teams, title='Teams')

@app.route('/<int:unterwb>/<int:spieltag>')
def teamtabelle(unterwb, spieltag):
    cur = g.db.execute("SELECT MAX(ls.Spieltag) FROM Ligaspiel ls INNER JOIN Spiel s ON s.SPielID = ls.SpielID WHERE s.UnterwbID = ?", [unterwb])
    max_spieltag = cur.fetchall()[0][0]
    cur = g.db.execute(" \
    SELECT (SELECT CASE WHEN T1Tref = 6 THEN CASE WHEN T2Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T1Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg1, \
(SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID) AS T1, \
T1Tref, T2Tref, \
(SELECT Name From Team WHERE Team.TeamID = Spiel.Team2ID) AS T2, \
(SELECT CASE WHEN T2Tref = 6 THEN CASE WHEN T1Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T2Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg2 \
FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spieltag = ? AND UnterwbID = ? ", [spieltag, unterwb])
    table_st = [dict(Erg1=row[0], T1=row[1], T1tref=row[2], T2tref=row[3], T2=row[4], Erg2=row[5]) for row in cur.fetchall()]
    cur = g.db.execute("SELECT (SELECT Name FROM Team WHERE Team.TeamID = t2.TeamID) As Team, \
SUM(CASE WHEN t2.TeamID = t1.TeamID THEN 1 ELSE 0 END) Spiele, \
SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer END) Treffer, \
SUM(CASE WHEN Kassiert IS NULL THEN 0 ELSE Kassiert END) Kassiert, \
SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer-Kassiert END) AS Differenz, \
SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 1 ELSE 0 END) AS G,\
SUM(CASE WHEN Treffer < 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS V, \
SUM(CASE WHEN Treffer = 6 AND Kassiert = 5 THEN 1 ELSE 0 END) AS OTS, \
SUM(CASE WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS OTN, \
SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 3 WHEN Treffer = 6 AND Kassiert = 5 THEN 2 WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS Punkte \
FROM \
(SELECT DISTINCT TeamID FROM Teilgenommen WHERE Teilgenommen.UnterwbID = ?) AS t2 Left Join \
(SELECT Spiel.SpielID, Team1ID TeamID, T1Tref Treffer, T2Tref Kassiert, Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 AND Spiel.UnterwbID = ? AND Spieltag <= ? UNION SELECT Spiel.SpielID, Team2ID TeamID, T2Tref Treffer, T1Tref Kassiert, Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 AND Spiel.UnterwbID = ? AND Spieltag <= ?) AS t1 \
ON t2.TeamID = t1.TeamID \
GROUP BY t2.TeamID \
ORDER BY Punkte DESC, Differenz DESC, Treffer DESC, Team ASC;", [unterwb, unterwb, spieltag, unterwb, spieltag])
    table_t = [dict(team=row[0], spiele=row[1], treffer=row[2], kassiert=row[3], diff=row[4], g=row[5], v=row[6], ots=row[7], otn=row[8], punkte=row[9])for row in cur.fetchall()]

    return render_template('tabellen.html', title='Teamtabelle', max_spieltag=max_spieltag, table_st=table_st, table_t=table_t, unterwb=unterwb, spieltag=spieltag)



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
