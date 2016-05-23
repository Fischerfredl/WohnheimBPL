from flask import request, flash, current_app, session
from functions_general import query_db, update_db, get_last_id, verify_password, set_password, set_new_password, \
    get_users
from competition.functions import get_league_game_result


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
        if not session['gameid']:
            form_input = [('Kein Spiel gewaehlt', 'label', 'label', '')]
        elif session['username'] != 'mod' and query_db('SELECT SiegerID FROM Spiel WHERE SpielID = ?', [session['gameid']], one=True):
            form_input = [('Spiel bereits eingetragen', 'label', 'label', '')]
        else:
            result = get_league_game_result(session['gameid'])
            var = [0, 1, 2, 3, 4, 5, 6]
            divisionid = query_db('SELECT UnterwbID FROM Spiel WHERE SpielID = ?', [result[0]], one=True)
            form_input = [('SpielID: %i'%result[0], 'label', 'label', ''),
                          (result[2]+' treffer', 'select_list', 't1tref', var),
                          ('Spieler1', 'select_list', 'sp1', get_players(result[2], divisionid)),
                          ('Spieler1 treffer', 'select_list', 'sp1tref', var),
                          ('Spieler2', 'select_list', 'sp2', get_players(result[2], divisionid)),
                          ('Spieler2 treffer', 'select_list', 'sp2tref', var),
                          (result[5]+' treffer', 'select_list', 't2tref', var),
                          ('Spieler3', 'select_list', 'sp3', get_players(result[5], divisionid)),
                          ('Spieler3 treffer', 'select_list', 'sp3tref', var),
                          ('Spieler4', 'select_list', 'sp4', get_players(result[5], divisionid)),
                          ('Spieler4 treffer', 'select_list', 'sp4tref', var)]
    elif option == 'sql_query':
        form_input = [('Query', 'text', 'query', '')]
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
        'team_edit': 'Team bearbeiten',
        'sql_query': 'SQL-Query'
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
    if not session['gameid']:
        flash('error: no game')
        return False
    gameid = session['gameid']
    t1tref = int(request.form['t1tref'])
    t2tref = int(request.form['t2tref'])
    sp1 = request.form['sp1']
    sp2 = request.form['sp2']
    sp3 = request.form['sp3']
    sp4 = request.form['sp4']
    sp1id = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [sp1], one=True)
    sp2id = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [sp2], one=True)
    sp3id = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [sp3], one=True)
    sp4id = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [sp4], one=True)
    sp1tref = int(request.form['sp1tref'])
    sp2tref = int(request.form['sp2tref'])
    sp3tref = int(request.form['sp3tref'])
    sp4tref = int(request.form['sp4tref'])
    if t1tref == 6 and t2tref == 6 or t1tref != 6 and t2tref != 6:
        flash('error: no winning team')
        return False
    if sp1tref+sp2tref > t1tref:
        flash('error: team 1 players to much cups')
        return False
    if sp3tref+sp4tref > t2tref:
        flash('error: team 2 players too much cups')
        return False
    if sp1 == sp2:
        flash('error: identical players in team 1')
        return False
    if sp3 == sp4:
        flash('error: identical players in team 2')
        return False
    if t1tref == 6:
        winner = query_db('SELECT Team1ID FROM Spiel WHERE SpielID = ?', [gameid], one=True)
    else:
        winner = query_db('SELECT Team2ID FROM Spiel WHERE SpielID = ?', [gameid], one=True)
    update_db('UPDATE Spiel SET SiegerID = ? WHERE SpielID = ?', [winner, gameid])
    update_db('UPDATE Ligaspiel SET T1Tref = ? WHERE SpielID = ?', [t1tref, gameid])
    update_db('UPDATE Ligaspiel SET T2Tref = ? WHERE SpielID = ?', [t2tref, gameid])
    update_db('DELETE FROM Ligaspieler WHERE SpielID = ?', [gameid])
    update_db('INSERT INTO Ligaspieler(SpielID, SpielerID, Treffer) VALUES (?, ?, ?)', [gameid, sp1id, sp1tref])
    update_db('INSERT INTO Ligaspieler(SpielID, SpielerID, Treffer) VALUES (?, ?, ?)', [gameid, sp2id, sp2tref])
    update_db('INSERT INTO Ligaspieler(SpielID, SpielerID, Treffer) VALUES (?, ?, ?)', [gameid, sp3id, sp3tref])
    update_db('INSERT INTO Ligaspieler(SpielID, SpielerID, Treffer) VALUES (?, ?, ?)', [gameid, sp4id, sp4tref])
    flash('Spiel eingetragen')
    return True


def get_players(teamname, divisionid):
    return [row[0] for row in query_db('SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Teilgenommen.SpielerID) \
              FROM Teilgenommen WHERE TeamID = (SELECT TeamID FROM Team WHERE Name = ?) AND UnterwbID = ?', [teamname, divisionid])]


def sql_query():
    query = request.form['query']
    error = update_db(query)
    if error:
        flash(error)
    else:
        flash('Erfolg')
    return
