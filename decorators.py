from functools import wraps
from flask import session, abort
from functions_general import query_db


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        nickname = kwargs['nickname']
        if not session['logged_in']:
            abort(403, 'Nicht eingeloggt')
        elif session['username'] != nickname:
            abort(403, 'Nicht eingeloggt als user: %s' % nickname)
        return f(*args, **kwargs)
    return decorated_function


def login_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session['logged_in']:
            abort(403, 'Nicht eingeloggt')
        elif session['username'] != 'admin':
            abort(403, 'Nicht eingeloggt als admin')
        return f(*args, **kwargs)
    return decorated_function


def login_mod_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session['logged_in']:
            abort(403, 'Nicht eingeloggt')
        elif session['username'] != 'mod':
            abort(403, 'Nicht eingeloggt als mod')
        return f(*args, **kwargs)
    return decorated_function


def check_competition(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not query_db('SELECT * FROM Wettbewerb WHERE WbID = ?',
                        [kwargs['competitionid']], one=True):
            abort(404, 'Wettbewerb nicht vorhanden')
        return f(*args, **kwargs)
    return decorated_function


def check_division(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not query_db('SELECT * FROM Unterwettbewerb WHERE UnterwbID = ?',
                        [kwargs['divisionid']], one=True):
            abort(404, 'Unterwettbewerb nicht vorhanden')
        return f(*args, **kwargs)
    return decorated_function


def check_league(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not query_db('SELECT * FROM Unterwettbewerb WHERE Modus = "liga" AND UnterwbID = ?',
                        [kwargs['leagueid']], one=True):
            abort(404, 'Liga nicht vorhanden')
        return f(*args, **kwargs)
    return decorated_function


def check_league_matchday(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        matchday = kwargs['matchday']
        max_matchday = query_db('SELECT MAX(Spieltag) \
                                FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                                WHERE UnterwbID = ?', [kwargs['leagueid']], one=True)
        if not query_db('SELECT * FROM Unterwettbewerb WHERE Modus = "liga" AND UnterwbID = ?',
                        [kwargs['leagueid']], one=True):
            abort(404, 'Liga nicht vorhanden')
        elif matchday < 1 or matchday > max_matchday:
            abort(404, 'Spieltag existiert nicht')
        return f(*args, **kwargs)
    return decorated_function


def check_game(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not query_db('SELECT * FROM Spiel WHERE SpielID = ?', [kwargs['gameid']], one=True):
            abort(404, 'Spiel existiert nicht')
        return f(*args, **kwargs)
    return decorated_function


def check_player(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not query_db('SELECT * FROM Spieler WHERE Nickname = ?', [kwargs['nickname']], one=True):
            abort(404, 'Spieler existiert nicht')
        return f(*args, **kwargs)
    return decorated_function


def check_team(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not query_db('SELECT * FROM Team WHERE Name = ?', [kwargs['teamname']], one=True):
            abort(404, 'Spieler existiert nicht')
        return f(*args, **kwargs)
    return decorated_function



