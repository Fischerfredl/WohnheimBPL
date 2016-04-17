from flask import g, abort, session
from functools import wraps


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0][0] if rv else None) if one else rv


def update_db(query, args=()):
    g.db.execute(query, args)
    g.db.commit()
    return


def get_users():
    userlist = []
    for user in query_db('SELECT Nickname FROM Spieler'):
        userlist.append(user[0])
    return userlist


def get_teams():
    teamlist = []
    for team in query_db('SELECT Name FROM Team'):
        teamlist.append(team[0])
    return teamlist


def login_required(user=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user:
                if not session['loged_in']:
                    abort(403, 'Nicht eingeloggt')
            else:
                if session['username'] != user:
                    abort(403, 'Nicht eingeloggt als user: %s' % user)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
