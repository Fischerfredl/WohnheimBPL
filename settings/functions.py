from flask import request, flash, current_app, session, abort, redirect, url_for
from functions_general import query_db, update_db, verify_password, set_password, set_new_password, \
    get_users, get_new_id
from competition.functions import get_league_game_result
from random import shuffle


# label, type, name, value
def get_form(option):
    form_input = []
    if option == 'player_new':
        form_input = [('Nickname', 'text', 'nickname', '')]
    elif option == 'player_del':
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
        form_input = [('Teamname', 'text', 'teamname', '')]
    elif option == 'team_del':
        form_input = [('Teamname', 'select_list', 'teamname',
                       [row[0] for row in query_db('SELECT name FROM Team t \
                                                   WHERE t.TeamID NOT IN (SELECT TeamID FROM Teilgenommen)')])]
    elif option == 'team_edit':
        pass
    elif option == 'competition_create':
        form_input = [('Name', 'text', 'competition_name', '')]
    elif option == 'competition_make':
        form_input = [('Wettbewerb', 'select_list', 'competition_name',
                       [row[0] for row in query_db("SELECT Name FROM Wettbewerb WHERE Phase = 'anmeldung'")]),
                      ('Modus', 'select_list', 'modus', ['Liga - eine Gruppe'])]
    elif option == 'competition_advance':
        pass
    elif option == 'competition_close':
        form_input = [('Wettbewerb', 'select_list', 'competition_name',
                       [row[0] for row in query_db("SELECT Name FROM Wettbewerb WHERE Phase = 'laeuft'")])]
    elif option == 'competition_reopen':
        form_input = [('Wettbewerb', 'select_list', 'competition_name',
                       [row[0] for row in query_db("SELECT Name FROM Wettbewerb WHERE Phase = 'beendet'")])]
    elif option == 'competition_reset':
        form_input = [('Wettbewerb', 'select_list', 'competition_name',
                       [row[0] for row in query_db("SELECT Name FROM Wettbewerb WHERE Phase = 'laeuft'")])]
    elif option == 'competition_delete':
        form_input = [('Wettbewerb', 'select_list', 'competition_name',
                       [row[0] for row in query_db("SELECT Name FROM Wettbewerb WHERE Phase != 'beendet'")])]
    elif option == 'competition_player_assign':
        form_input = [('Unterwettbewerb', 'select_list', 'division',
                       [row[0] for row in query_db("SELECT Name FROM Unterwettbewerb WHERE (SELECT Phase FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID) != 'beendet'")]),
                      ('Spieler', 'select_list', 'nickname',
                       [row[0] for row in query_db("SELECT Nickname FROM Spieler")]),
                      ('Team', 'select_list', 'name',
                       [row[0] for row in query_db("SELECT Name FROM Team")])]
    elif option == 'competition_player_unassign':
        form_input = [('Unterwettbewerb', 'select_list', 'division',
                       [row[0] for row in query_db("SELECT Name FROM Unterwettbewerb WHERE (SELECT Phase FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID) != 'beendet'")]),
                      ('Spieler', 'select_list', 'nickname',
                       [row[0] for row in query_db("SELECT Nickname FROM Spieler")])]
    elif option == 'player_assign_team':
        form_input = [('Spieler', 'select_list', 'nickname',
                       [row[0] for row in query_db("SELECT Nickname FROM Spieler")]),
                      ('Team', 'select_list', 'teamname',
                       [row[0] for row in query_db("SELECT Name FROM Team")])]
    elif option == 'game_edit':
        if not session.get('gameid'):
            form_input = [('Waehle ein Spiel', 'select_list', 'gameid',
                           [row[0] for row in query_db("SELECT SpielID FROM Spiel")])]
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
            if session['username'] != 'mod' and (session['username'] not in get_players(result[2], divisionid) and session['username'] not in get_players(result[5], divisionid)):
                return abort(401)
    elif option == 'sql_query':
        form_input = [('Query', 'text', 'query', '')]
    elif option == 'set_adminpassword':
        form_input = [('Passwort', 'text', 'input', '')]
    elif option == 'set_modpassword':
        form_input = [('Passwort', 'text', 'input', '')]
    elif option == 'set_secret_key':
        form_input = [('Key', 'text', 'input', '')]
    elif option == 'set_salt':
        form_input = [('Salt', 'text', 'input', '')]
    elif option == 'division_rename':
        form_input = [
            ('Unterwettbewerb', 'select_list', 'division_name', [row[0] for row in query_db("SELECT Name FROM Unterwettbewerb WHERE (SELECT Phase FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID) = 'laeuft'")]),
            ('Name', 'text', 'name', '')
        ]
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
        'competition_reset': 'Wettbewerb zuruecksetzen',
        'competition_delete': 'Wettbewerb loeschen',
        'competition_player_assign': 'Spieler zu Wettbewerb anmelden',
        'competition_player_unassign': 'Spieler von Wettbewerb abmelden',
        'player_assign_team': 'Spieler: Team zuweisen',
        'game_edit': 'Spiel bearbeiten',
        'player_edit': 'Spieler bearbeiten',
        'player_reset_password': 'Spieler: Passwort zuruecksetzen',
        'player_set_password': 'Passwort setzen',
        'team_edit': 'Team bearbeiten',
        'sql_query': 'SQL-Query',
        'set_adminpassword': 'Admin-Passwort setzen',
        'set_modpassword': 'Mod-Passwort setzen',
        'set_secret_key': 'Secret-Key setzen',
        'set_salt': 'Salt setzen',
        'division_rename': 'Unterwettbewerb umbenennen'
    }


def get_options_by_permission():
    options = []
    settings = current_app.config['SETTINGS']
    admin = current_app.config['ADMINLOGIN']
    mod = current_app.config['MODLOGIN']
    for option in settings:
        if session['username'] in settings[option] or 'signed_user' in settings[option] and session['logged_in'] \
                and session['username'] != admin and session['username'] != mod:
            if option != 'game_edit':
                options.append(option)
    return sorted(options)


def player_new():
    nickname = request.form['nickname']
    if nickname == 'mod' or nickname == 'admin':
        flash('Name %s ungueltig' % nickname)
        return False

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
    flash('Daten geaendert')
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
    competition_id = get_new_id('competition')
    v = update_db("INSERT INTO Wettbewerb(WbID, Name, Phase) VALUES (?, ?, 'anmeldung')", [competition_id, competition_name])
    if v:
        flash(v)
        return False
    flash('Wettbewerb %s angelegt' % competition_name)
    division_name = competition_name + ' - Anmeldung'
    v = update_db("INSERT INTO Unterwettbewerb(WbID, Name) VALUES (?, ?)", [competition_id, division_name])
    if v:
        flash(v)
        return False
    flash('Unterwettbewerb %s angelegt' % division_name)
    return True


def competition_make():
    modus = request.form['modus']
    competition_name = request.form['competition_name']
    competition_id = query_db('SELECT WbID FROM Wettbewerb WHERE Name = ?', [competition_name], one=True)
    division_id = query_db('SELECT UnterwbID FROM Unterwettbewerb WHERE WbID = ?', [competition_id], one=True)
    dict_backup = dict()
    for row in query_db('SELECT TeamID, SpielerID FROM Teilgenommen WHERE UnterwbID = ?', [division_id]):
        if row[0] not in dict_backup:
            dict_backup[row[0]] = []
        dict_backup[row[0]].append(row[1])
    list_teams = [key for key in dict_backup]

    for key in dict_backup:
        if len(dict_backup[key]) < 2:
            flash('Wettbewerb nicht gestartet')
            flash('Mindestens ein Team hat zu wenig Spieler')
            return False

    if modus == 'Liga - eine Gruppe':
        if len(list_teams) < 2:
            flash('Wettbewerb nicht gestartet')
            flash('Zu wenig Teams angemeldet')
            return False
        make_spielplan(division_id, list_teams)
        update_db("UPDATE Unterwettbewerb SET Modus = 'liga' WHERE UnterwbID = ?", [division_id])
        update_db("UPDATE Unterwettbewerb SET Name = ? WHERE UnterwbID = ?", [competition_name + ' - Gruppe1', division_id])
    elif modus == 'Liga - zwei Gruppen':
        v = update_db('DELETE FROM Unterwettbewerb WHERE UnterwbID = ?', [division_id])
        if v:
            flash(v)
        v = update_db('DELETE FROM Teilgenommen WHERE UnterwbID = ?', [division_id])
        if v:
            flash(v)
    update_db("UPDATE Wettbewerb SET Phase = 'laeuft' WHERE WbID = ?", [competition_id])
    flash('Wettbewerb ' + competition_name + ' erfolgreich gestartet')
    return True

def competition_advance():
    return


def competition_close():
    competition_name = request.form['competition_name']
    v = update_db("UPDATE Wettbewerb SET Phase = 'beendet' WHERE Name = ?", [competition_name])
    if v:
        flash(v)
        return False
    flash('Wettbewerb ' + competition_name + ' erfolgreich beendet')
    return True


def competition_reopen():
    competition_name = request.form['competition_name']
    v = update_db("UPDATE Wettbewerb SET Phase = 'laeuft' WHERE Name = ?", [competition_name])
    if v:
        flash(v)
        return False
    flash('Wettbewerb ' + competition_name + ' erfolgreich wieder geoeffnet')
    return True

def competition_reset():
    competition_name = request.form['competition_name']
    competition_id = query_db("SELECT WbID FROM Wettbewerb WHERE Name = ?", [competition_name], one=True)

    v = update_db("UPDATE Wettbewerb SET Phase = 'anmeldung' WHERE WbID = ?", [competition_id])
    if v:
        flash(v)
        return False

    division_ids = [row[0] for row in query_db("SELECT UnterwbID FROM Unterwettbewerb WHERE WbID = ?", [competition_id])]

    new_div_id = get_new_id('division')
    div_name = competition_name + ' - Anmeldung'
    v = update_db("INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name) VALUES (?, ?, ?)", [new_div_id, competition_id, div_name])
    if v:
        flash(v)
        return False

    for div_id in division_ids:
        for row in query_db("SELECT SpielerID, TeamID FROM Teilgenommen WHERE UnterwbID = ?", [div_id]):
            update_db("INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES(?, ?, ?)", [new_div_id, row[1], row[0]])

        v = update_db("DELETE FROM Teilgenommen WHERE UnterwbID = ?", [div_id])
        if v:
            flash(v)
            return False
        for game_id in [row[0] for row in query_db("SELECT SpielID FROM Spiel WHERE UnterwbID = ?", [div_id])]:
            v = update_db("DELETE FROM KOSpiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Ligaspieler WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Ligaspiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Turnierspiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Spiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
        v = update_db("DELETE FROM Unterwettbewerb WHERE UnterwbID = ?", [div_id])
        if v:
            flash(v)
            return False
    flash('Wettbewerb erfolgreich zurueckgesetzt')
    return True


def competition_delete():
    competition_name = request.form['competition_name']
    competition_id = query_db("SELECT WbID FROM Wettbewerb WHERE Name = ?", [competition_name], one=True)
    division_ids = [row[0] for row in query_db("SELECT UnterwbID FROM Unterwettbewerb WHERE WbID = ?", [competition_id])]
    for div_id in division_ids:
        v = update_db("DELETE FROM Teilgenommen WHERE UnterwbID = ?", [div_id])
        if v:
            flash(v)
            return False
        for game_id in [row[0] for row in query_db("SELECT SpielID FROM Spiel WHERE UnterwbID = ?", [div_id])]:
            v = update_db("DELETE FROM KOSpiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Ligaspieler WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Ligaspiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Turnierspiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
            v = update_db("DELETE FROM Spiel WHERE SpielID = ?", [game_id])
            if v:
                flash(v)
                return False
        v = update_db("DELETE FROM Unterwettbewerb WHERE UnterwbID = ?", [div_id])
        if v:
            flash(v)
            return False
    v = update_db("DELETE FROM Wettbewerb WHERE WbID = ?", [competition_id])
    if v:
        flash(v)
        return False
    flash('Wettbewerb ' + competition_name + ' erfolgreich geloescht')
    return True


def competition_player_assign():
    division_name  = request.form['division']
    player = request.form['nickname']
    team = request.form['name']

    div_id = query_db("SELECT UnterwbID FROM Unterwettbewerb WHERE Name = ?", [division_name], one=True)
    player_id = query_db("SELECT SpielerID FROM Spieler WHERE Nickname = ?", [player], one=True)
    team_id = query_db("SELECT teamID FROM Team WHERE Name = ?", [team], one=True)

    check = query_db("SELECT (SELECT Name FROM Team WHERE Team.TeamID = Teilgenommen.TeamID) FROM Teilgenommen WHERE UnterwbID = ? AND SpielerID = ?", [div_id, player_id], one=True)
    if check:
        flash('Spieler %s ist bereits mit Team %s an Wettbewerb %s angemeldet' % (player, check, division_name))
        return False

    v = update_db("INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES(?, ?, ?)", [div_id, team_id, player_id])
    if v:
        flash(v)
        return False
    flash('Spieler %s mit Team %s erfolgreich zu Unterwettbewerb %s angemeldet' % (player, team, division_name))
    return True


def competition_player_unassign():
    division_name = request.form['division']
    player = request.form['nickname']

    div_id = query_db("SELECT UnterwbID FROM Unterwettbewerb WHERE Name = ?", [division_name], one=True)
    player_id = query_db("SELECT SpielerID FROM Spieler WHERE Nickname = ?", [player], one=True)

    team_id = query_db("SELECT TeamID FROM Teilgenommen WHERE UnterwbID = ? AND SpielerID = ?", [div_id, player_id], one=True)
    if not team_id:
        flash('Spieler %s ist nicht an Wettbewerb %s angemeldet' % (player, division_name))
        return False

    phase = query_db("SELECT (SELECT Phase FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID) FROM Unterwettbewerb WHERE UnterwbID = ?", [div_id], one=True)
    if len(query_db("SELECT * FROM Teilgenommen WHERE UnterwbID = ? AND TeamID = ?", [div_id, team_id])) < 3 and phase != 'anmeldung':
        flash('Zu wenige Spieler im Team, um den Spieler abzumelden')
        return False

    v = update_db("DELETE FROM Teilgenommen WHERE UnterwbID = ? AND SpielerID = ?", [div_id, player_id])
    if v:
        flash(v)
        return False
    flash('Spieler %s erfolgreich von Unterwettbewerb %s abgemeldet' % (player, division_name))
    return True


def player_assign_team():
    return


def game_edit():
    if not session.get('gameid'):
        session['gameid'] = request.form['gameid']
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


def make_spielplan(division_id, list_teams):
    if len(list_teams) % 2 != 0:
        list_teams.append(-1)
    shuffle(list_teams)
    anzahl = len(list_teams)
    i = 1
    while i < anzahl:
        temp1 = i
        temp2 = anzahl
        if temp1 % 2 != 0:
            j = temp1
            temp1 = temp2
            temp2 = j
        if list_teams[temp1-1] != -1 and list_teams[temp2-1] != -1:
            make_ligaspiel(get_new_id('game'), division_id, i, list_teams[temp1-1], list_teams[temp2-1])
        k = 1
        while k < (anzahl / 2):
            temp1 = (i + k) % (anzahl - 1)
            temp2 = (i - k) % (anzahl - 1)
            if temp2 <= 0:
                temp2 += (anzahl - 1)
            if temp1 == 0:
                temp1 = anzahl - 1
            if temp1 % 2 != 1:
                j = temp1
                temp1 = temp2
                temp2 = j
            if list_teams[temp1-1] != -1 and list_teams[temp2-1] != -1:
                make_ligaspiel(get_new_id('game'), division_id, i, list_teams[temp1-1], list_teams[temp2-1])
            k += 1
        flash('Spieltag %i angelegt!' % i)
        i += 1
    flash('Spielplan fertig')
    return


def make_ligaspiel(id, div_id, st, t1, t2):
    v = update_db("INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID) VALUES (?, ?, ?, ?) ", [id, div_id, t1, t2])
    if v:
        flash(v)
    v = update_db("INSERT INTO Ligaspiel(SpielID, Spieltag) VALUES (?, ?)", [id, st])
    if v:
        flash(v)
    return

def set_adminpassword():
    current_app.config['ADMINPASSWORD'] = request.form['input']
    flash('Adminpasswort gesetzt zu %s' % request.form['input'])
    return


def set_modpassword():
    current_app.config['MODPASSWORD'] = request.form['input']
    flash('Modpasswort gesetzt zu %s' % request.form['input'])
    return


def set_secret_key():
    current_app.config['SECRET_KEY'] = request.form['input']
    flash('Secret Key gesetzt zu %s' % request.form['input'])
    return


def set_salt():
    current_app.config['SALT'] = request.form['input']
    flash('Salt gesetzt zu %s' % request.form['input'])
    return


def division_rename():
    div_name = request.form['division_name']
    new_name = request.form['name']

    v = update_db("UPDATE Unterwettbewerb SET Name = ? WHERE Name = ?", [new_name, div_name])

    if v:
        flash(v)
        return False
    flash('Unterwettbewerb erfolgreich umbenannt')
    return True
