from functions_general import query_db, update_db, get_users, get_teams, abort
from flask import flash, current_app
from hashlib import sha1
import random
import string


def get_new_id(entity):
    return {
        'player': query_db('SELECT MAX(SpielerID) FROM Spieler', one=True)+1,
        'team': query_db('SELECT MAX(TeamID) FROM Team', one=True)+1,
        'competition': query_db('SELECT MAX(WbID) FROM Wettbewerb', one=True)+1,
        'division': query_db('SELECT MAX(UnterwbID) FROM Unterwettbewerb', one=True)+1,
        'game': query_db('SELECT MAX(SpielID) FROM Spiel', one=True)+1
    }[entity]


def get_items(option):
    itemlist = []
    if option == 'del_player':
        for row in query_db('SELECT nickname FROM Spieler s \
                            WHERE s.SpielerID NOT IN (SELECT SpielerID FROM Teilgenommen)'):
            itemlist.append(row[0] )
    elif option == 'del_team':
        for row in query_db('SELECT name FROM Team t \
                            WHERE t.TeamID NOT IN (SELECT TeamID FROM Teilgenommen)'):
            itemlist.append(row[0])
    elif option == 'new_password':
        itemlist = get_users()
    return itemlist


def new_player(nickname, name, vorname):
    if len(nickname) == 0 or nickname in get_users():
        flash('Spieler nicht angelegt')
        flash('Spielername nicht akzeptiert oder bereits vorhanden')
        return False
    else:
        new_id = get_new_id('player')
        update_db('INSERT INTO Spieler(SpielerID, Nickname, Name, Vorname) VALUES (?, ?, ?, ?)',
                  [new_id, nickname, name, vorname])
        if nickname not in get_users():
            flash('Spieler nicht angelgegt')
            flash('Konnte nicht in Datenbank eingetragen werden')
            return False
        flash('Spieler erfolgreich angelegt')
        flash('Werte: (%i, %s, %s, %s)' % (new_id, nickname, name, vorname))
        return True


def new_team(name):
    if len(name) == 0 or name in get_teams():
        flash('Team nicht angelegt')
        flash('Teamname nicht akzeptiert oder bereits vorhanden')
        return False
    else:
        new_id = get_new_id('team')
        update_db('INSERT INTO Team(TeamID, Name) VALUES (?, ?)', [new_id, name])
        if name not in get_teams():
            flash('Team nicht angelegt')
            flash('Konnte nicht in Datenbank eingetragen werden')
            return False
        flash('Team erfolgreich angelegt')
        flash('Werte: (%i, %s)' % (new_id, name))
        return True


def del_player(nickname):
    if nickname not in get_users():
        flash('Spieler konnte nicht geloescht werden')
        flash('Spieler nicht in Datenbank')
        return False
    update_db('DELETE FROM Spieler WHERE nickname = ?', [nickname])
    if nickname in get_users():
        flash('Spieler konnte nicht geloescht werden')
        flash('Spieler nach loeschversuch weiterhin in Datenbank')
        return False
    flash('Spieler %s erfolgreich geloescht' % nickname)
    return True


def del_team(name):
    if name not in get_teams():
        flash('Team konnte nicht geloescht werden')
        flash('Team nicht in Datenbank')
        return False
    update_db('DELETE FROM Team WHERE name = ?', [name])
    if name in get_teams():
        flash('Team konnte nicht geloescht werden')
        flash('Team nach loeschversuch weiterhin in Datenbank')
        return False
    flash('Team %s erfolgreich geloescht' % name)
    return True


def new_password(nickname):
    if nickname not in get_users():
        flash('Passwort nicht neu gesetzt')
        flash('Spieler nicht in Datenbank')
        return False
    password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
    update_db("UPDATE Spieler SET Passwort = ? WHERE Nickname = ?",
              [sha1(password+current_app.config['SALT']).hexdigest(), nickname])
    test1 = query_db('SELECT Passwort FROM Spieler WHERE Nickname = ?', [nickname])
    test2 = sha1(password+current_app.config['SALT']).hexdigest()
    if query_db('SELECT Passwort FROM Spieler WHERE Nickname = ?', [nickname], one=True) != \
            sha1(password+current_app.config['SALT']).hexdigest():
        flash('Passwort fehlerhaft neu gesetzt')
        flash('Fehler in der Datenbankanfrage')
        return False
    flash('Passwort erfolgreich neu gesetzt')
    flash('Username: %s, Passwort %s' % (nickname, password))
    return True


def get_table_body(view):
    if view == 'player':
        return query_db('SELECT * FROM Spieler')
    elif view == 'team':
        return query_db('SELECT * FROM Team')
    elif view == 'game':
        return query_db('SELECT * FROM Spiel')
    elif view == 'competition':
        return query_db('SELECT * FROM Wettbewerb')
    elif view == 'division':
        return query_db('SELECT * FROM Unterwettbewerb')
    elif view == 'participated':
        return query_db('SELECT * FROM Teilgenommen')
    else:
        return abort(500, 'In admin functions get_table error')
