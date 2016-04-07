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
# Route: COMP
#
# ----------------------------------------------------------------------------------------------------------------------
#
# Navigation for comp-route:
# comp ->
# comp/compid->
# comp/compid/teams OR comp/leagueid/spieltag OR comp/groupid OR comp/koid
#
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# General comp
# ----------------------------------------------------------------------------------------------------------------------

@app.route('/comp')
def comp():
    table = query_db('SELECT WbID, Name FROM Wettbewerb')
    return render_template('comp.html', table=table)


@app.route('/comp/<int:compid>')
def compdetail(compid):
    if not query_db('SELECT * FROM Wettbewerb WHERE WbID = ?', [compid], one=True):
        return error_handler('Wettbewerb nicht vorhanden')
    compname = query_db('SELECT Name FROM Wettbewerb WHERE WbID = ?', [compid], one=True)
    table_unterwb = query_db("SELECT UnterwbID, Name, Modus FROM Unterwettbewerb WHERE WbID = ?", [compid])
    return render_template('compdetail.html', compid=compid, compname=compname, table_unterwb=table_unterwb)


# ----------------------------------------------------------------------------------------------------------------------
# Team view
# ----------------------------------------------------------------------------------------------------------------------

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


@app.route('/comp/unterwb/<int:unterwb>/teams')
def unterwbteams(unterwb):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE UnterwbID = ?', [unterwb], one=True):
        return error_handler('Unterwettbewerb nicht vorhanden')
    unterwbname = query_db('SELECT Name FROM Unterwettbewerb WHERE UnterwbID = ?', [unterwb], one=True)
    query = query_db('SELECT DISTINCT (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) AS teamn, \
                     (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = tg.SpielerID) AS spielern \
                     FROM Teilgenommen tg \
                     WHERE UnterwbID = ?', [unterwb])
    table = dict()
    for row in query:
        if row[0] not in table:
            table[row[0]] = []
        table[row[0]].append(row[1])
    return render_template('unterwbteams.html', unterwbid=unterwb, unterwbname=unterwbname, table=table)


# ----------------------------------------------------------------------------------------------------------------------
# Unterwettbewerbe
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/comp/unterwb/<int:unterwb>')
def unterwettbewerb(unterwb):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE UnterwbID = ?', [unterwb], one=True):
        return error_handler('Unterwettbewerb nicht vorhanden')
    unterwbinfo = getUnterwbInfo(unterwb)
    table_spiele = []
    for spielid in query_db('SELECT SpielID FROM Spiel WHERE UnterwbID = ?', [unterwb]):
            table_spiele.append(getSpielErgebnis(spielid[0]))
    if unterwbinfo[2] == 'liga':
        return redirect(url_for('league', leagueid=unterwb, spieltag=getCurrentSpieltag(unterwb)))
    elif unterwbinfo[2] == 'turnier':
        return render_template('group.html', unterwbinfo=unterwbinfo, table_spiele=table_spiele)
    else:
        return render_template('ko.html', unterwbinfo=unterwbinfo, table_spiele=table_spiele)


@app.route('/comp/liga/<int:leagueid>/<int:spieltag>')
def league(leagueid, spieltag):
    if not query_db('SELECT * FROM Unterwettbewerb WHERE UnterwbID = ?', [leagueid], one=True):
        return error_handler('Liga nicht vorhanden')
    max_spieltag = getMaxSpieltag(leagueid)
    if spieltag < 1 or spieltag > max_spieltag:
        return error_handler('Spieltag existiert nicht')
    unterwbinfo = getUnterwbInfo(leagueid)
    table_teamtabelle = getLigaTeamtabelle(leagueid, spieltag)
    table_spielertabelle = getSpielertabelle(leagueid, spieltag)
    table_spiele = []
    for spielid in query_db('SELECT Spiel.SpielID FROM Spiel Inner Join Ligaspiel ON Spiel.SpielID = Ligaspiel.SpielID \
                            WHERE Spiel.UnterwbID = ? AND Ligaspiel.Spieltag = ?', [leagueid, spieltag]):
        table_spiele.append(getSpielErgebnis(spielid[0]))
    return render_template('league.html', unterwbinfo=unterwbinfo,
                           spieltag=spieltag, max_spieltag=max_spieltag,
                           table_teamtabelle=table_teamtabelle, table_spielertabelle=table_spielertabelle,
                           table_spiele=table_spiele)

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
    return render_template('detailteam.html', teamname=teamname, teamid=teamid, teaminfo=teaminfo)


@app.route('/player/<nickname>')
def detailplayer(nickname):
    if not query_db('SELECT * FROM Spieler WHERE Nickname = ?', [nickname]):
        return error_handler('Spieler gibbet nich')
    data = query_db('SELECT SpielerID, Nickname, Vorname, Name FROM Spieler WHERE Nickname = ?', [nickname])[0]
    spielerinfo = getSpielerinfo(nickname)
    return render_template('detailplayer.html', nickname=nickname, data=data, spielerinfo=spielerinfo)


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
# Route: login view
#
# ----------------------------------------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if not validatePassword(user, password) and \
                not(user == app.config['ADMINLOGIN'] and password == app.config['ADMINPASSWORD']) and \
                not(user == app.config['MODLOGIN'] and password == app.config['ADMINPASSWORD']):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            session['username'] = user
            flash('You were logged in: %s' % user)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('home'))


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
@app.route('/player/<nickname>/settings/<option>', methods=['GET', 'POST'])
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


# returns LigaTeamtabelle - List with tuples: Team, Spiele, Treffer, Kassiert, Diff, G, V, OTS, OTN, Punkte
def getLigaTeamtabelle(unterwb, spieltag):
    return query_db("SELECT (SELECT Name FROM Team WHERE Team.TeamID = t2.TeamID) As Team, \
                      SUM(CASE WHEN t2.TeamID = t1.TeamID THEN 1 ELSE 0 END) Spiele, \
                      SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer END) Treffer, \
                      SUM(CASE WHEN Kassiert IS NULL THEN 0 ELSE Kassiert END) Kassiert, \
                      SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer-Kassiert END) AS Differenz, \
                      SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 1 ELSE 0 END) AS G,\
                      SUM(CASE WHEN Treffer < 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS V, \
                      SUM(CASE WHEN Treffer = 6 AND Kassiert = 5 THEN 1 ELSE 0 END) AS OTS, \
                      SUM(CASE WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS OTN, \
                      SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 3 WHEN Treffer = 6 AND Kassiert = 5 THEN 2 \
                        WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS Punkte \
                    FROM \
                      (SELECT DISTINCT TeamID FROM Teilgenommen WHERE Teilgenommen.UnterwbID = ?) AS t2 Left Join \
                      (SELECT Spiel.SpielID, Team1ID TeamID, T1Tref Treffer, T2Tref Kassiert, \
                        Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet \
                        FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                        WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 \
                          AND Spiel.UnterwbID = ? AND Spieltag <= ? \
                      UNION \
                      SELECT Spiel.SpielID, Team2ID TeamID, T2Tref Treffer, T1Tref Kassiert, \
                        Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet \
                        FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                        WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 \
                          AND Spiel.UnterwbID = ? AND Spieltag <= ?) AS t1 \
                    ON t2.TeamID = t1.TeamID \
                    GROUP BY t2.TeamID \
                    ORDER BY Punkte DESC, Differenz DESC, Treffer DESC, Team ASC;",
                    [unterwb, unterwb, spieltag, unterwb, spieltag])


# returns Spielertabelle - List with tuples: Nickname, Treffer, Spiele, Diff
def getSpielertabelle(unterwb, spieltag):
    return [dict(name=row[0], treffer=row[1], spiele=row[2], schnitt=round(float(row[1])/row[2], 2)) for row in
            query_db("SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = ls.SpielerID), \
                    SUM(treffer) AS Treffer, \
                    COUNT(*) AS Spiele \
                    FROM (Ligaspieler ls LEFT JOIN Spiel s ON ls.SpielID = s.SpielID) \
                    LEFT JOIN Ligaspiel lsp ON lsp.SpielID = s.SpielID \
                    WHERE s.UnterwbID = ? AND lsp.Spieltag <= ? \
                    GROUP BY ls.SpielerID ORDER BY treffer DESC, Spiele ASC", [unterwb, spieltag])]


def getMaxSpieltag(unterwb):
    return query_db('SELECT MAX(Spieltag) \
                    FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                    WHERE UnterwbID = ?', [unterwb], one=True)


def getCurrentSpieltag(unterwb):
    maxst = getMaxSpieltag(unterwb)
    while maxst != 1:
        if query_db('SELECT SiegerID \
FROM Spiel Inner Join Ligaspiel ON Spiel.SpielID = Ligaspiel.SpielID \
WHERE Spieltag = ? AND UnterwbID = ? AND SiegerID not null', [maxst, unterwb], one=True):
            return maxst
        maxst -= maxst
    return 1


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


# returns tuple (UntewbID, Name, Modus, WbID, WbName)
def getUnterwbInfo(unterwb):
    return query_db('SELECT UnterwbID, \
                           Name, \
                           Modus, \
                           WbID, \
                           (SELECT Name FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID) \
                           FROM Unterwettbewerb WHERE UnterwbID = ?',
                           [unterwb])[0]



# returns SpielErgebnis depending on type:
# Ligaspiel-tuple: (SpielID, Erg1, Team1, T1Tref, T2Tref, T2, Erg2, Spieltag, spielerlist[]:tuples (spieler, treffer)})
# Turnierspiel - tuple: (SpielID, Team1, Team2, Sieger, Becherueber)
# KOSpiel - tuple: (SpielID, Team1, Erg1, Erg2, Team2)
def getSpielErgebnis(gameid):
    modus = query_db('SELECT (SELECT Modus FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID) \
                     FROM Spiel Where SpielID = ?', [gameid], one=True)
    if modus == 'liga':
        gametuple = query_db("SELECT Spiel.SpielID, \
                 (SELECT CASE WHEN T1Tref = 6 THEN CASE WHEN T2Tref = 5 THEN 'OTS' ELSE 'G' END \
                   ELSE CASE WHEN T1Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg1, \
                 (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID) AS T1, \
                 T1Tref, T2Tref, \
                 (SELECT Name From Team WHERE Team.TeamID = Spiel.Team2ID) AS T2, \
                 (SELECT CASE WHEN T2Tref = 6 THEN CASE WHEN T1Tref = 5 THEN 'OTS' ELSE 'G' END \
                   ELSE CASE WHEN T2Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg2, \
                 Ligaspiel.Spieltag \
                 FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SpielID = ? ",
                 [gameid])[0]
        spielerlist = []
        for spieler in query_db('SELECT \
                                (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Ligaspieler.SpielerID), \
                                Treffer FROM Ligaspieler WHERE SpielID = ? ', [gameid]):
            spielerlist.append(spieler)
        gametuple = gametuple + (spielerlist, )
        return gametuple
    elif modus == 'turnier':
        return query_db('SELECT Spiel.SpielID, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID), \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team2ID), \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.SiegerID), \
                    Becherueber \
                    FROM Spiel Inner Join Turnierspiel ON Spiel.SpielID = Turnierspiel.SpielID \
                    WHERE Spiel.SpielID = ?', [gameid])[0]
    else:  # modus =='ko'
        return query_db('SELECT Spiel.SpielID, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID), \
                    T1Erg, \
                    T2Erg, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team2ID) \
                    FROM Spiel Inner Join KOspiel ON Spiel.SpielID = KOspiel.SpielID \
                    WHERE Spiel.SpielID = ?', [gameid])[0]


# returns Spieldata - tuple: (SpielID, UnterwbID, Unterwbname, Datum, Gewertet)
def getSpieldata(gameid):
    return query_db('SELECT Spiel.SpielID, UnterwbID, \
                    (SELECT Name FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID), \
                    Datum, Gewertet FROM Spiel WHERE SpielID = ?',
                    [gameid])[0]


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


def validatePassword(nickname, pass1):
    pass2 = query_db('SELECT Passwort FROM Spieler WHERE Nickname = ?', [nickname], one=True)
    if sha1(pass1+'salt#!!!?1256').hexdigest() == pass2:
        return True
    else:
        return False


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
# player functions
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
