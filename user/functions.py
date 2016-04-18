from flask import flash, session
from functions_general import query_db, update_db, set_password, verify_password, get_users
from competition.functions import get_league_teamtable, get_league_matchday_current


def get_player_data(playername):
    return query_db('SELECT SpielerID, Nickname, Vorname, Name FROM Spieler WHERE Nickname = ?', [playername])[0]


def get_player_history(playername):
    history = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name, \
                        (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE SpielerID = (SELECT SpielerID FROM Spieler WHERE nickname = ?)', [playername]):
        divisionid = row[0]
        divisionname = row[2]
        team = row[3]
        if row[1] == 'liga':
            rank = get_league_teamrank(divisionid, team)
        else:
            # row[1] == 'ko'
            rank = 'Platzierung fuer KO nicht implementiert'
        line = (divisionid, divisionname, rank, team)
        history.append(line)
    return history


def get_team_data(teamname):
    return query_db('SELECT TeamID, Name FROM Team WHERE Name = ?', [teamname])[0]


def get_team_history(teamname):
    history = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE TeamID = (SELECT TeamID FROM Team WHERE name = ?)', [teamname]):
        divisionid = row[0]
        divisionname = row[2]
        if row[1] == 'liga':
            rank = get_league_teamrank(divisionid, teamname)
        else:
            # row[1] == 'ko'
            rank = 'Platzierung fuer KO nicht implementiert'
        spieler = query_db('SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Teilgenommen.SpielerID) \
                           FROM Teilgenommen \
                           WHERE UnterwbID = ? AND \
                           (SELECT name FROM Team WHERE Team.TeamID = Teilgenommen.TeamID) = ?', [divisionid, teamname])
        line = (divisionid, divisionname, rank, spieler)
        history.append(line)
    return history


def get_league_teamrank(leagueid, team):
    i = 1
    for item in get_league_teamtable(leagueid, get_league_matchday_current(leagueid)):
        if item[0] == team:
            return i
        i += 1
    return 0


def new_personal_info(nickname, vorname, nachname):
    if not len(vorname) == 0:
        update_db('UPDATE Spieler SET Vorname = ? WHERE Nickname = ?', [vorname, nickname])
    if not len(nachname) == 0:
        update_db('UPDATE Spieler SET Name = ? WHERE Nickname = ?', [nachname, nickname])
    data_new = query_db('SELECT vorname, name FROM Spieler WHERE Nickname = ?', [nickname])[0]
    flash('Persoenliche Daten geaendert')
    flash('Werte: (%s, %s, %s)' % (nickname, data_new[0], data_new[1]))
    return True


def new_password(nickname, pwold, pwnew):
    if not verify_password(nickname, pwold):
        flash('Passwort nicht neu gesetzt')
        flash('Altes Passwort nicht korrekt')
        return False
    if len(pwnew) < 3:
        flash('Passwort nicht neu gesetzt')
        flash('Passwort nicht lang genug')
        return False
    set_password(nickname, pwnew)
    if not verify_password(nickname, pwnew):
        flash('Passwort nicht neu gesetzt')
        flash('Fehler in der Datenbankabfrage')
        return False
    flash('Passwort neu gesetzt')
    flash('Username: %s, Passwort: %s' % (nickname, pwnew))
    return True


def new_nickname(nickold, password, nicknew):
    if not verify_password(nickold, password):
        flash('Neuer Nick nicht gesetzt')
        flash('Passwort nicht korrekt')
        return False
    if nicknew in get_users():
        flash('Neuer Nick nicht gesetzt')
        flash('Nick existiert bereits')
        return False
    update_db('UPDATE Spieler SET Nickname = ? WHERE Nickname = ?', [nicknew, nickold])
    if nicknew not in get_users():
        flash('Neuer Nick nicht gesetzt')
        flash('Fehler in Datenbankabfrage')
        return False
    session['username'] = nicknew
    flash('Neuer Nick %s gesetzt' % nicknew)
    return True
