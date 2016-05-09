from functools import wraps
from flask import session, abort, current_app
from functions_general import query_db


def login_required(user=None):
    def inner_function(f):
        if not user:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not session['logged_in']:
                    abort(403, 'Nicht eingeloggt')
                return f(*args, **kwargs)
            return decorated_function
        elif user == 'designated':
            @wraps(f)
            def decorated_function(*args, **kwargs):
                nickname = kwargs['nickname']
                if not session['logged_in']:
                    abort(403, 'Nicht eingeloggt')
                elif session['username'] != nickname:
                    abort(403, 'Nicht eingeloggt als user: %s' % nickname)
                return f(*args, **kwargs)
            return decorated_function

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session['logged_in']:
                abort(403, 'Nicht eingeloggt')
            elif session['username'] != user:
                abort(403, 'Nicht eingeloggt als admin')
            return f(*args, **kwargs)
        return decorated_function
    return inner_function


def settings_permission_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        permission = current_app.config['SETTINGS'].get(kwargs['option'], None)
        if not permission:
            abort(404, 'Einstellung nicht gefunden')
        if 'signed_user' in permission and not session['logged_in']:
            abort(403, 'Nicht eingeloggt')
        if 'signed_user' not in permission and session.get('username', None) not in permission:
            abort(403, 'Fehlende Berechtigung fuer diese Einstellungen')
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


def check_competition_phase(phase):
    def inner_function(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if phase != query_db('SELECT Phase FROM Wettbewerb WHERE WbID = ?', [kwargs['competitionid']], one=True):
                abort(404, 'Wettbewerb nicht in Anmeldephase')
            return f(*args, **kwargs)
        return decorated_function
    return inner_function
