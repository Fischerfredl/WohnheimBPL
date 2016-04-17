import os
import sqlite3
import platform
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from contextlib import closing
from config import config_linux, config_windows
from hashlib import sha1


app = Flask(__name__)


if platform.system() == 'Linux':
    app.config.from_object(config_linux)
elif platform.system() == 'Windows':
    app.config.from_object(config_windows)

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
    if not query_db('SELECT * FROM Team WHERE Name = ?', [teamname], one=True):
        return error_handler('Team nicht vorhanden')
    teamid = query_db('SELECT TeamID FROM Team WHERE Name = ?', [teamname], one=True)
    teaminfo = getTeaminfo(teamname)
    return render_template('detail_team.html', teamname=teamname, teamid=teamid, teaminfo=teaminfo)


@app.route('/user/<nickname>')
def detailplayer(nickname):
    if not query_db('SELECT * FROM Spieler WHERE Nickname = ?', [nickname]):
        return error_handler('Spieler gibbet nich')
    data = query_db('SELECT SpielerID, Nickname, Vorname, Name FROM Spieler WHERE Nickname = ?', [nickname])[0]
    spielerinfo = getSpielerinfo(nickname)
    return render_template('detail_player.html', nickname=nickname, data=data, spielerinfo=spielerinfo)


@app.route('/game/<int:gameid>')
def detailgame(gameid):
    if not query_db('SELECT * FROM Spiel WHERE SpielID = ?', [gameid]):
        return error_handler('Spiel gibbet nich')
    modus = query_db('SELECT (SELECT Modus FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID) \
                     FROM Spiel Where SpielID = ?', [gameid], one=True)
    data = getSpieldata(gameid)
    ergebnis = [getSpielErgebnis(gameid)]
    return render_template('detailgame.html', gameid=gameid, modus=modus, data=data, ergebnis=ergebnis)


# ----------------------------------------------------------------------------------------------------------------------
#
# admin view
#
# ----------------------------------------------------------------------------------------------------------------------

@app.route('/admin')
def admin():
    if not verifylogin(user='admin'):
        return error_handler('Not logged in as admin')
    return render_template('admin.html')


# allowed for option:
# newplayer, newteam, resetpw, delplayer, delteam
@app.route('/admin/settings/<option>', methods=['GET', 'POST'])
def adminsettings(option):
    if not verifylogin(user='admin'):
        return error_handler('Not logged in as admin')
    error = None
    dellist = []
    if request.method == 'POST':
        if option == 'newplayer':
            if not trynewplayer(request.form['nickname'], request.form['name'], request.form['vorname']):
                error = 'Spieler konnte nicht angelegt werden'
            else:
                flash('Spieler angelegt. Nick: %s, Name: %s, Vorname: %s' %
                      (request.form['nickname'], request.form['name'], request.form['vorname']))
                return redirect(url_for('admin'))
        elif option == 'newteam':
            if not trynewteam(request.form['name']):
                error = 'Team konnte nicht angelegt werden'
            else:
                flash('Team angelegt. Name: %s ' % request.form['name'])
                return redirect(url_for('admin'))
        elif option == 'delplayer':
            if not trydelplayer(request.form['nickname']):
                error = 'Spieler konnte nicht geloescht werden'
            else:
                flash('Spieler geloescht. Name: %s' % request.form['nickname'])
                return redirect(url_for('admin'))
        elif option == 'delteam':
            if not trydelteam(request.form['name']):
                error = 'Team konnte nicht geloescht werden'
            else:
                flash('Team geloescht. Name: %s' % request.form['name'])
                return redirect(url_for('admin'))
        elif option == 'resetpw':  # option == 'resetpw'
            if not tryresetpw(request.form['nickname']):
                error = 'Passwort konnte nicht zurueckgesetzt werden'
            else:
                flash('Passwort zurueckgesetzt. Spieler: %s' % request.form['nickname'])
                return redirect(url_for('admin'))
        else:
            error_handler('Einstellungen gibbet nich')
    else:  # request.method == 'GET'
        if option == 'delplayer':
            for row in query_db('SELECT nickname FROM Spieler s \
                                WHERE s.SpielerID NOT IN (SELECT SpielerID FROM Teilgenommen)'):
                dellist.append(row[0])
        if option == 'delteam':
            for row in query_db('SELECT name FROM Team t \
                                WHERE t.TeamID NOT IN (SELECT TeamID FROM Teilgenommen)'):
                dellist.append(row[0])
        if option == 'resetpw':
            dellist = getUsers()
    return render_template('adminsettings.html', error=error, option=option, dellist=dellist)

# ----------------------------------------------------------------------------------------------------------------------
#
# settings
#
# ----------------------------------------------------------------------------------------------------------------------


# allowed for otion
# persona, password
@app.route('/user/<nickname>/settings/<option>', methods=['GET', 'POST'])
def playersettings(nickname, option):
    if not query_db('SELECT * FROM Spieler WHERE nickname = ?', [nickname]):
        error_handler('Spieler gibbet nich')
    if not verifylogin(user=nickname):
        error_handler('Nicht eingeloggt als %s' % nickname)
    error = None
    if request.method == 'POST':
        if option == 'personal':
            if not trychangepersonal(nickname, request.form['name'], request.form['vorname']):
                error = 'Daten konnten nicht geaendert werden'
            else:
                flash('Daten geaendert. Spieler: %s, Name: %s, Vorname: %s' %
                      (nickname, request.form['name'], request.form['vorname']))
                return redirect(url_for('detailplayer', nickname=nickname))
        elif option == 'password':
            if not trychangepw(nickname, request.form['pwold'], request.form['pwnew']):
                error = 'Passwort konnte nicht geaendert werden'
            else:
                flash('Passwort geaendert')
                return redirect(url_for('detailplayer', nickname=nickname))
        elif option == 'nickname':
            if not trychangenick(nickname, request.form['password'], request.form['nicknew']):
                return error_handler('Nick konnte nicht geaendert werden')
            else:
                flash('Nickname geaendert von %s in %s' % (nickname, request.form['nicknew']))
                session['username'] = request.form['nicknew']
                return redirect(url_for('detailplayer', nickname=request.form['nicknew']))
        else:
            return error_handler('Einstellung gibbet nich')
    # else:  # request.method == 'GET'
    return render_template('playersettings.html', error=error, option=option, nickname=nickname)


# ----------------------------------------------------------------------------------------------------------------------
#
# dev layout
#
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/dev/home')
def dev_home():
    return render_template('dev/home.html')


@app.route('/dev/comp')
def dev_comp():
    table = query_db('SELECT WbID, Name FROM Wettbewerb')
    return render_template('dev/comp.html', table=table)


@app.route('/dev/comp/<int:compid>')
def dev_compdetail(compid):
    if not query_db('SELECT * FROM Wettbewerb WHERE WbID = ?', [compid], one=True):
        return error_handler('Wettbewerb nicht vorhanden')
    compname = query_db('SELECT Name FROM Wettbewerb WHERE WbID = ?', [compid], one=True)
    table_unterwb = query_db("SELECT UnterwbID, Name, Modus FROM Unterwettbewerb WHERE WbID = ?", [compid])
    return render_template('dev/compdetail.html', compid=compid, compname=compname, table_unterwb=table_unterwb)


@app.route('/dev/comp/unterwb/<int:unterwb>')
def dev_unterwettbewerb(unterwb):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE UnterwbID = ?', [unterwb], one=True):
        return error_handler('Unterwettbewerb nicht vorhanden')
    modus = query_db('SELECT Modus FROM Unterwettbewerb WHERE UnterwbID = ?', [unterwb], one=True)
    if modus == 'liga':
        return redirect(url_for('league', leagueid=unterwb, spieltag=getCurrentSpieltag(unterwb)))
    elif modus == 'turnier':
        return redirect(url_for('gruppe', groupid=unterwb))
    else:
        return redirect(url_for('ko', koid=unterwb))


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#
# Custom functions
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def getLigaplatzierung(unterwb, team):
    i = 1
    for item in getLigaTeamtabelle(unterwb, getCurrentSpieltag(unterwb)):
        if item[0] == team:
            return i
        i += 1
    return 0


# returns Teaminfo - List with tuples: (UnterwbID, Unterwbname, Platzierung, (Spieler,))
def getTeaminfo(team):
    infolist = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE TeamID = (SELECT TeamID FROM Team WHERE name = ?)', [team]):
        unterwbid = row[0]
        unterwbname = row[2]
        if row[1] == 'liga':
            platz = getLigaplatzierung(unterwbid, team)
        else:
            # row[1] == 'ko'
            platz = 'Platzierung fuer KO nicht implementiert'
        spieler = query_db('SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Teilgenommen.SpielerID) \
                           FROM Teilgenommen \
                           WHERE UnterwbID = ? AND \
                           (SELECT name FROM Team WHERE Team.TeamID = Teilgenommen.TeamID) = ?', [unterwbid, team])
        platzierung = (unterwbid, unterwbname, platz, spieler)
        infolist.append(platzierung)
    return infolist


# returns Spielerinfo - List with tuples: (UnterwbID, Unterwbname, Platzierung, Team)
def getSpielerinfo(spieler):
    infolist = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name, \
                        (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE SpielerID = (SELECT SpielerID FROM Spieler WHERE nickname = ?)', [spieler]):
        unterwbid = row[0]
        unterwbname = row[2]
        team = row[3]
        if row[1] == 'liga':
            platz = getLigaplatzierung(unterwbid, team)
        else:
            # row[1] == 'ko'
            platz = 'Platzierung fuer KO nicht implementiert'
        platzierung = (unterwbid, unterwbname, platz, team)
        infolist.append(platzierung)
    return infolist




# ----------------------------------------------------------------------------------------------------------------------
# Login function
# ----------------------------------------------------------------------------------------------------------------------

def getUsers():
    userlist = []
    for item in query_db('SELECT Nickname FROM Spieler'):
        userlist.append(item[0])
    return userlist

def getTeams():
    teamlist = []
    for item in query_db('SELECT Name FROM Team'):
        teamlist.append(item[0])
    return teamlist


def setPassword(nickname, password):
    update_db("UPDATE Spieler SET Passwort = ? WHERE Nickname = ?", [sha1(password+'salt#!!!?1256').hexdigest(), nickname])
    return

def verifylogin(user=None):
    if not session['logged_in']:
        return False
    elif not user:
        return True
    elif session['username'] == user:
        return True
    else:
        return False


# ----------------------------------------------------------------------------------------------------------------------
# admin functions
# ----------------------------------------------------------------------------------------------------------------------

def trynewplayer(nickname, name, vorname):
    if len(nickname) == 0 or nickname in getUsers():
        return False
    else:
        update_db('INSERT INTO Spieler(SpielerID, Nickname, Name, Vorname) VALUES (?, ?, ?, ?)',
                  [getSpielerID(), nickname, name, vorname])
        if nickname not in getUsers():
            return False
        return True


def trynewteam(name):
    if len(name) == 0 or name in getTeams():
        return False
    else:
        update_db('INSERT INTO Team(TeamID, Name) VALUES (?, ?)',
                  [getTeamID(), name])
        if name not in getTeams():
            return False
        return True


def trydelplayer(nickname):
    if nickname not in getUsers():
        return False
    update_db('DELETE FROM Spieler WHERE nickname = ?', [nickname])
    if nickname in getUsers():
        return False
    return True


def trydelteam(name):
    if name not in getTeams():
        return False
    update_db('DELETE FROM Team WHERE name = ?', [name])
    if name in getTeams():
        return False
    return True


def tryresetpw(nickname):
    if nickname not in getUsers():
        return False
    setPassword(nickname, app.config['DEFAULTPASS'])
    if not validatePassword(nickname, app.config['DEFAULTPASS']):
        return False
    return True

# ----------------------------------------------------------------------------------------------------------------------
# user functions
# ----------------------------------------------------------------------------------------------------------------------


def trychangepersonal(nickname, vorname, nachname):
    if nickname not in getUsers():
        return False
    if not len(vorname) == 0:
        update_db('UPDATE Spieler SET Vorname = ? WHERE Nickname = ?', [vorname, nickname])
    if not len(nachname) == 0:
        update_db('UPDATE Spieler SET Name = ? WHERE Nickname = ?', [nachname, nickname])
    return True


def trychangepw(nickname, pwold, pwnew):
    if not validatePassword(nickname, pwold):
        return False
    if len(pwnew) < 3:
        return False
    setPassword(nickname, pwnew)
    if not validatePassword(nickname, pwnew):
        return False
    return True


def trychangenick(nickold, password, nicknew):
    if not validatePassword(nickold, password):
        return False
    if nicknew in getUsers():
        return False
    update_db('UPDATE Spieler SET Nickname = ? WHERE Nickname = ?', [nicknew, nickold])
    if nicknew not in getUsers():
        return False
    return True

# ----------------------------------------------------------------------------------------------------------------------
# Get IDs
# ----------------------------------------------------------------------------------------------------------------------


def getSpielerID():
    return query_db('SELECT MAX(SpielerID) FROM Spieler', one=True)+1


def getTeamID():
    return query_db('SELECT MAX(TeamID) FROM Team', one=True)+1


def getWettbewerbID():
    return query_db('SELECT MAX(WettbewerbID) FROM Wettbewerb', one=True)+1


def getUnterwettbewerbID():
    return query_db('SELECT MAX(UnterwettbewerbID) FROM Unterwettbewerb', one=True)+1


def getSpielID():
    return query_db('SELECT MAX(SpielID) FROM Spiel', one=True)+1


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
# general functions
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0][0] if rv else None) if one else rv


def update_db(query, args=()):
    g.db.execute(query, args)
    g.db.commit()
    return


def error_handler(error):
    return render_template('notfound.html', error=error)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#
# Running app from console
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host=app.config['IPADDR'], port=app.config['PORT'])
