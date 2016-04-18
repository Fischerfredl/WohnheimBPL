from flask import g, current_app
import random
import string
from hashlib import sha1


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0][0] if rv else None) if one else rv


def update_db(query, args=()):
    g.db.execute(query, args)
    g.db.commit()
    return


def get_new_id(entity):
    return {
        'player': query_db('SELECT MAX(SpielerID) FROM Spieler', one=True)+1,
        'team': query_db('SELECT MAX(TeamID) FROM Team', one=True)+1,
        'competition': query_db('SELECT MAX(WbID) FROM Wettbewerb', one=True)+1,
        'division': query_db('SELECT MAX(UnterwbID) FROM Unterwettbewerb', one=True)+1,
        'game': query_db('SELECT MAX(SpielID) FROM Spiel', one=True)+1
    }[entity]


def get_users():
    entitylist = []
    for entity in query_db('SELECT Nickname FROM Spieler'):
        entitylist.append(entity[0])
    return entitylist


def get_teams():
    entitylist = []
    for entity in query_db('SELECT Name FROM Team'):
        entitylist.append(entity[0])
    return entitylist

def get_competitions():
    entitylist = []
    for entity in query_db('SELECT Name FROM Wettbewerb'):
        entitylist.append(entity[0])
    return entitylist



def set_new_password(nickname):
    password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
    set_password(nickname, password)
    return password


def set_password(nickname, password):
    if not check_password(password):
        return False
    else:
        update_db("UPDATE Spieler SET Passwort = ? WHERE Nickname = ?",
              [sha1(password+current_app.config['SALT']).hexdigest(), nickname])
        return True


def verify_password(nickname, password):
    if query_db('SELECT Passwort FROM Spieler WHERE Nickname = ?', [nickname], one=True) != \
            sha1(password+current_app.config['SALT']).hexdigest():
        return False
    return True


# to do: check for valid password
def check_password(password):
    if len(password) < 3:
        return False
    return True
