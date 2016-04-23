from flask import flash
from functions_general import get_new_id, get_competitions, update_db, query_db


def new_competition(name):
    if name in get_competitions():
        flash('Wettbewerb nicht erzeugt')
        flash('Name bereits vorhanden')
        return False
    competition_id = get_new_id('competition')
    update_db("INSERT INTO Wettbewerb(WbID, Name, Phase) VALUES (?, ?, 'anmeldung')", [competition_id, name])
    flash('Wettbewerb %s angelegt' % name)
    division_id = get_new_id('division')
    division_name = name + ' - Anmeldung'
    update_db("INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN) VALUES (?, ?, ?, 'anmeldung', 'ein')",
              [division_id, competition_id, division_name])
    flash('Unterwettbewerb %s angelegt' % division_name)
    return True


def get_registration_division(competitionid):
    return query_db('SELECT UnterwbID FROM Unterwettbewerb WHERE WbID = ?', [competitionid], one=True)


def get_player_registration(nickname, competitionid):
    divisionid = get_registration_division(competitionid)
    return query_db('SELECT \
                    (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) \
                    FROM Teilgenommen tg \
                    WHERE tg.SpielerID = (SELECT SpielerID FROM Spieler WHERE Nickname = ?) AND UnterwbID = ?',
                    [nickname, divisionid], one=True)


def register_player(nickname, divisionid, teamname):
    if get_player_registration(nickname, divisionid):
        flash('Spieler nicht angemeldet')
        flash('Spieler bereits fuer Unterwettbewerb registriert')
        return False
    playerid = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [nickname], one=True)
    teamid = query_db('SELECT TeamID FROM Team WHERE name = ?', [teamname], one=True)
    update_db('INSERT INTO Teilgenommen(UnterwbID, SpielerID, TeamID) VALUES (?, ?, ?)', [divisionid, playerid, teamid])
    competitionid = query_db('SELECT WbID FROM Unterwettbewerb WHERE UnterwbID = ?', [divisionid], one=True)
    if not get_player_registration(nickname, competitionid):
        flash('Spieler nicht angemeldet')
        flash('Fehler in Datenbankanfrage')
        return False
    flash('Spieler %s angemeldet' % nickname)
    flash('Team: %s' % teamname)
    return True


def unregister_player(nickname, competitionid):
    divisionid = get_registration_division(competitionid)
    if not get_player_registration(nickname, competitionid):
        flash('Spieler nicht abgemeldet')
        flash('Spieler war nicht eingetragen')
        return False
    playerid = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [nickname], one=True)
    update_db('DELETE FROM Teilgenommen WHERE UnterwbID = ? AND SpielerID = ?', [divisionid, playerid])
    if get_player_registration(nickname, competitionid):
        flash('Spieler nicht abgemeldet')
        flash('Fehler in Datenbankabfrage')
        return False
    return True


def delete_competition(competitionid):
    if not query_db('SELECT * FROM Wettbewerb WHERE WbID = ?', [competitionid]):
        flash('Wettbewerb nicht geloescht')
        flash('Wettbewerb nicht vorhanden')
        return False
    for divisionid in query_db('SELECT UnterwbID FROM Unterwettbewerb WHERE WbID = ?', [competitionid]):
        update_db('DELETE FROM Teilgenommen WHERE UnterwbID = ?', [divisionid[0]])
        for gameid in query_db('SELECT SpielID FROM Spiel WHERE UnterwbID = ?', [divisionid[0]]):
            update_db('DELETE FROM KOSpiel WHERE SpielID = ?', [gameid[0]])
            update_db('DELETE FROM Ligaspiel WHERE SpielID = ?', [gameid[0]])
            update_db('DELETE FROM Ligaspieler WHERE SpielID = ?', [gameid[0]])
            update_db('DELETE FROM Turnierspiel WHERE SpielID = ?', [gameid[0]])
            update_db('DELETE FROM Spiel WHERE SpielID = ?', [gameid[0]])
        update_db('DELETE FROM Unterwettbewerb WHERE UnterwbID = ?', [divisionid[0]])
    update_db('DELETE FROM Wettbewerb WHERE WbID = ?', [competitionid])
    flash('Wettbewerb mit ID: %s geloescht' % competitionid)
    return True


def get_items(option):
    itemlist = dict()
    if option == 'del_competition':
        for row in query_db('SELECT WbID, Name FROM Wettbewerb'):
            itemlist[row[0]] = row[1]
    return itemlist
