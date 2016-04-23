from flask import request, flash, current_app, session
from functions_general import query_db, update_db, get_last_id


def get_form(option):
    form_input = []
    if option == 'new_player':
        form_input = [('Nickname', 'text', 'nickname', '')]
    return [{'label': row[0], 'type': row[1], 'name': row[2], 'value': row[3]} for row in form_input]


def get_header():
    return {
        'new_player': 'Neuen Spieler anlegen',
        'new_team': 'Neues Team anlegen',
        'del_player': 'Spieler loeschen',
        'del_team': 'Team loeschen',
        'create_competition': 'Wettbewerb anlegen',
        'make_competition': 'Wettbewerb starten',
        'advance_competition': 'KO-Runde fortschalten',
        'close_competition': 'Wettbewerb abschliessen',
        'reopen_competition': 'Wettbewerb bearbeiten',
        'delete_competition': 'Wettbewerb loeschen',
        'player_assign_team': 'Team einem Wettbewerb hinzufuegen',
        'edit_game': 'Spiel bearbeiten',
        'edit_player': 'Spieler bearbeiten',
        'edit_player_reset_password': 'Passwort zuruecksetzen',
        'edit_player_set_password': 'Passwort setzen',
        'edit_team': 'Team bearbeiten'
    }


def get_options_by_permission():
    options = []
    settings = current_app.config['SETTINGS']
    for option in settings:
        if session.username in settings[option] or 'signed_user' in settings[option] and session['logged_in']:
            options.append(option)
    return options

def new_player():
    nickname = request.form['nickname']
    v = update_db('INSERT INTO Spieler(Nickname) VALUES (?)', [nickname])
    if v:
        flash(v)
        return False
    flash('Neuer Spieler %s angelegt' % nickname)
    return True


def new_team():
    teamname = request.form['teamname']
    v = update_db('INSERT INTO Team(Name) VALUES (?)', [teamname])
    if v:
        flash(v)
        return False
    flash('Neues Team %s angelegt' % teamname)
    return True


def del_player():
    nickname = request.form['nickname']
    v = update_db('DELETE FROM Spieler WHERE Nickname = ?', nickname)
    if v:
        flash(v)
        return False
    flash('Spieler %s geloescht' % nickname)
    return True


def del_team():
    teamname = request.form['teamname']
    v = update_db('DELETE FROM TEAM WHERE Name = ?', [teamname])
    if v:
        flash(v)
        return False
    flash('Team %s geloescht' % teamname)
    return True


def create_competition():
    competition_name = request.form['competition_name']
    v = update_db("INSERT INTO Wettbewerb(Name, Phase) VALUES (?, 'anmeldung')", [competition_name])
    if v:
        flash(v)
        return False
    flash('Wettbewerb %s angelegt' % competition_name)
    competition_id = get_last_id()
    division_name = competition_name + ' - Anmeldung'
    v = update_db("INSERT INTO Unterwettbewerb(WbID, Name) VALUES (?, ?)", [competition_id, division_name])
    if v:
        flash(v)
        return False
    flash('Unterwettbewerb %s angelegt' % division_name)
    return True


def make_competition():
    return
def advance_competition():
    return
def close_competition():
    return
def reopen_competition():
    return
def delete_competition():
    return
def player_assign_team():
    return
def edit_game():
    return
def edit_player():
    return
def edit_player_reset_password():
    return
def edit_player_set_password():
    return
def edit_team():
    return