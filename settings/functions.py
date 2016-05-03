from flask import request, flash, current_app, session
from functions_general import query_db, update_db, get_last_id, verify_password, set_password, set_new_password, \
    get_users


def get_form(option):
    form_input = []
    if option == 'player_new':
        form_input = [('Nickname', 'text', 'nickname', '')]
    elif option == 'del_player':
        form_input = [('Nickname', 'select_list', 'nickname',
                       [row[0] for row in query_db('SELECT nickname FROM Spieler s \
                                                   WHERE s.SpielerID NOT IN (SELECT SpielerID FROM Teilgenommen)')])]
    elif option == 'player_edit':
        pass
    elif option == 'player_reset_password':
        form_input = [('Nickname', 'select_list', 'nickname', get_users())]
        pass
    elif option == 'player_set_password':
        pass
    elif option == 'team_new':
        pass
    elif option == 'team_del':
        pass
    elif option == 'team_edit':
        pass
    elif option == 'competition_create':
        pass
    elif option == 'competition_make':
        pass
    elif option == 'competition_advance':
        pass
    elif option == 'competition_close':
        pass
    elif option == 'competition_reopen':
        pass
    elif option == 'competition_delete':
        pass
    elif option == 'player_assign_team':
        pass
    elif option == 'game_edit':
        pass
    return [{'label': row[0], 'type': row[1], 'name': row[2], 'value': row[3]} for row in form_input]


def get_header():
    return {
        'player_new': 'Spieler: Neu anlegen',
        'team_new': 'Team: Neu anlegen',
        'player_del': 'Spieler: Loeschen',
        'team_del': 'Team: Loeschen',
        'competition_create': 'Wettbewerb anlegen',
        'competition_make': 'Wettbewerb starten',
        'competition_advance': 'Wettbewerb: KO-Runde fortschalten',
        'competition_close': 'Wettbewerb abschliessen',
        'competition_reopen': 'Wettbewerb bearbeiten',
        'competition_delete': 'Wettbewerb loeschen',
        'player_assign_team': 'Spieler: Team zuweisen',
        'game_edit': 'Spiel bearbeiten',
        'player_edit': 'Spieler bearbeiten',
        'player_reset_password': 'Spieler: Passwort zuruecksetzen',
        'player_set_password': 'Passwort setzen',
        'team_edit': 'Team bearbeiten'
    }


def get_options_by_permission():
    options = []
    settings = current_app.config['SETTINGS']
    admin = current_app.config['ADMINLOGIN']
    mod = current_app.config['MODLOGIN']
    for option in settings:
        if session['username'] in settings[option] or 'signed_user' in settings[option] and session['logged_in'] \
                and session['username'] != admin and session['username'] != mod:
            options.append(option)
    return sorted(options)


def player_new():
    nickname = request.form['nickname']
    v = update_db('INSERT INTO Spieler(Nickname) VALUES (?)', [nickname])
    if v:
        flash(v)
        return False
    flash('Neuer Spieler %s angelegt' % nickname)
    return True


def player_del():
    nickname = request.form['nickname']
    v = update_db('DELETE FROM Spieler WHERE Nickname = ?', nickname)
    if v:
        flash(v)
        return False
    flash('Spieler %s geloescht' % nickname)
    return True


def player_edit():
    nickname = session['username']
    nicknamenew = request.form['nicknamenew']
    name_first = request.form['name_first']
    name_last = request.form['name_last']
    v = query_db('UPDATE Spieler SET Nickname = ?, Name = ?, Vorname = ? WHERE Nickname = ?',
                 [nicknamenew, name_last, name_first, nickname])
    if v:
        flash('Daten nicht geaendert')
        flash(v)
        return False
    session['username'] = nicknamenew
    flash('Daten gesendert')
    return True


def player_reset_password():
    nickname = request.form['nickname']
    password = set_new_password(nickname)
    if not verify_password(nickname, password):
        flash('Error')
        return False
    flash('Passwort erfolgreich neu gesetzt')
    flash('Username: %s, Passwort %s' % (nickname, password))
    return True


def player_set_password():
    return


def team_new():
    teamname = request.form['teamname']
    v = update_db('INSERT INTO Team(Name) VALUES (?)', [teamname])
    if v:
        flash(v)
        return False
    flash('Neues Team %s angelegt' % teamname)
    return True


def team_del():
    teamname = request.form['teamname']
    v = update_db('DELETE FROM TEAM WHERE Name = ?', [teamname])
    if v:
        flash(v)
        return False
    flash('Team %s geloescht' % teamname)
    return True
def team_edit():
    return


def competition_create():
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


def competition_make():
    return
def competition_advance():
    return
def competition_close():
    return
def competition_reopen():
    return
def competition_delete():
    return
def player_assign_team():
    return
def game_edit():
    return


