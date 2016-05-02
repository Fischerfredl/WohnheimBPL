from functions_general import query_db, update_db, get_users, get_teams, verify_password, set_new_password, get_new_id
from flask import flash, abort


def get_items(option):
    itemlist = []
    if option == 'del_player':
        for row in query_db('SELECT nickname FROM Spieler s \
                            WHERE s.SpielerID NOT IN (SELECT SpielerID FROM Teilgenommen)'):
            itemlist.append(row[0])
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
    password = set_new_password(nickname)
    if not verify_password(nickname, password):
        flash('Passwort fehlerhaft neu gesetzt')
        flash('Fehler in der Datenbankanfrage')
        return False
    flash('Passwort erfolgreich neu gesetzt')
    flash('Username: %s, Passwort %s' % (nickname, password))
    return True



