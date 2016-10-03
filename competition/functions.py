from flask import abort, session, flash, g, current_app
from functions_general import query_db, update_db


# check_competition(competitionid)
# check_division(divisionid)
# check_league(leagueid)
# check_league_matchday(leagueid, matchday)
# get_competition_overview() - [(WbID, WbName)]
# get_competition_divisions(competitionid) - [(UnterwbID, Unterwbname, Modus)]
# get_competition_info(competitionid) - (WbId, Name, Phase)
# get_competition_teams(competitionid)
# get_division_teams(divisionid)
# get_division_info(divisionid) - (UntewbID, Name, Modus, WbID, WbName)
# get_division_mode(divisionid)
# get_group_games_info(divisionid)
# get_ko_games_info(divisionid)
# get_league_games_info(leagueid, matchday)
# get_league_teamtable(leagueid) - [(Team, Spiele, Treffer, Kassiert, Diff, G, V, OTS, OTN, Punkte)]
# get_league_playertable(leagueid) - [(Nickname, Treffer, Spiele, Diff)]
# get_league_matchday_max(leagueid)
# get_league_matchday_current(leagueid)
# get_league_game_result(gameid) - (SpielID, Erg1, Team1, T1Tref, T2Tref, T2, Erg2, Spieltag,
#                                   spielerlist[(spieler, treffer)]})
# get_group_game_result(gameid) - (SpielID, Team1, Team2, Sieger, Becherueber)
# get_ko_game_result(gameid) - (SpielID, Team1, Erg1, Erg2, Team2)


# ----------------------------------------------------------------------------------------------------------------------
#
# CHECK Functions
#
# ----------------------------------------------------------------------------------------------------------------------


def check_gamemode(gameid, modus):
    if modus != query_db('SELECT (SELECT Modus FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID) \
                          FROM Spiel Where SpielID = ?', [gameid], one=True):
        return abort(404, 'Spiel existiert nicht oder nicht von modus %s' % modus)


# ----------------------------------------------------------------------------------------------------------------------
#
# GET Functions
#
# ----------------------------------------------------------------------------------------------------------------------
# competition
# ----------------------------------------------------------------------------------------------------------------------


def get_competition_overview():
    nav = dict()
    for row in query_db("SELECT WbID, UnterwbID FROM Unterwettbewerb"):
        if row[0] not in nav:
            nav[row[0]] = []
        nav[row[0]].append(row[1])
    nav_compinfo = dict()
    for row in query_db("SELECT WbID, Name, Phase FROM Wettbewerb"):
        nav_compinfo[row[0]] = [row[1], row[2]]
    nav_divinfo = dict()
    for row in query_db("SELECT UnterwbID, Name, Modus FROM Unterwettbewerb"):
        nav_divinfo[row[0]] = [row[1], row[2]]

    session['nav'] = nav
    session['nav_compinfo'] = nav_compinfo
    session['nav_divinfo'] = nav_divinfo

    return query_db('SELECT WbID, Name FROM Wettbewerb')


def get_competition_divisions(competitionid):
    return query_db('SELECT UnterwbID, Name, Modus FROM Unterwettbewerb WHERE WbID = ?', [competitionid])


def get_competition_info(competitionid):
    return query_db('SELECT WbID, Name, Phase FROM Wettbewerb WHERE WbID = ?', [competitionid])[0]


# ----------------------------------------------------------------------------------------------------------------------
# teaminfo
# ----------------------------------------------------------------------------------------------------------------------


def get_competition_teams(competitionid):
    query = query_db('SELECT DISTINCT (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) AS teamn, \
                     (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = tg.SpielerID) AS spielern \
                     FROM Teilgenommen tg INNER JOIN Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                     WHERE uwb.WbID = ?', [competitionid])
    table = dict()
    for row in query:
        if row[0] not in table:
            table[row[0]] = []
        table[row[0]].append(row[1])
    return table


def get_division_teams(divisionid):
    query = query_db('SELECT DISTINCT (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) AS teamn, \
                     (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = tg.SpielerID) AS spielern \
                     FROM Teilgenommen tg \
                     WHERE UnterwbID = ?', [divisionid])
    table = dict()
    for row in query:
        if row[0] not in table:
            table[row[0]] = []
        table[row[0]].append(row[1])
    return table

# ----------------------------------------------------------------------------------------------------------------------
# division
# ----------------------------------------------------------------------------------------------------------------------


def get_division_info(divisionid):
    return query_db('SELECT uwb.UnterwbID, uwb.Name, uwb.Modus, wb.WbID, wb.Name\
                     FROM Unterwettbewerb uwb Inner Join Wettbewerb wb ON uwb.WbID = wb.WbID \
                     WHERE UnterwbID = ?', [divisionid])[0]


def get_division_mode(divisionid):
    return query_db('SELECT Modus FROM Unterwettbewerb WHERE UnterwbID = ?', [divisionid], one=True)


def get_group_games_info(divisionid):
    gamelist = []
    for gameid in query_db('SELECT SpielID FROM Spiel WHERE UnterwbID = ?', [divisionid]):
        gamelist.append(get_group_game_result(gameid[0]))
    return gamelist


def get_ko_games_info(divisionid):
    gamelist = []
    for gameid in query_db('SELECT SpielID FROM Spiel WHERE UnterwbID = ?', [divisionid]):
        gamelist.append(get_ko_game_result(gameid[0]))
    return gamelist

# ----------------------------------------------------------------------------------------------------------------------
# league
# ----------------------------------------------------------------------------------------------------------------------


def get_league_games_info(leagueid, matchday):
    gamelist = []
    for spielid in query_db('SELECT Spiel.SpielID FROM Spiel Inner Join Ligaspiel ON Spiel.SpielID = Ligaspiel.SpielID \
                            WHERE Spiel.UnterwbID = ? AND Ligaspiel.Spieltag = ?', [leagueid, matchday]):
        gamelist.append(get_league_game_result(spielid[0]))
    return gamelist


def get_league_teamtable(leagueid, matchday):
    return query_db("SELECT (SELECT Name FROM Team WHERE Team.TeamID = t2.TeamID) As Team, \
                      SUM(CASE WHEN t2.TeamID = t1.TeamID THEN 1 ELSE 0 END) Spiele, \
                      SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer END) Treffer, \
                      SUM(CASE WHEN Kassiert IS NULL THEN 0 ELSE Kassiert END) Kassiert, \
                      SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer-Kassiert END) AS Differenz, \
                      SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 1 ELSE 0 END) AS G,\
                      SUM(CASE WHEN Treffer < 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS V, \
                      SUM(CASE WHEN Treffer = 6 AND Kassiert = 5 THEN 1 ELSE 0 END) AS OTS, \
                      SUM(CASE WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS OTN, \
                      SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 3 WHEN Treffer = 6 AND Kassiert = 5 THEN 2 \
                        WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS Punkte \
                    FROM \
                      (SELECT DISTINCT TeamID FROM Teilgenommen WHERE Teilgenommen.UnterwbID = ?) AS t2 Left Join \
                      (SELECT Spiel.SpielID, Team1ID TeamID, T1Tref Treffer, T2Tref Kassiert, \
                        Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet \
                        FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                        WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 \
                          AND Spiel.UnterwbID = ? AND Spieltag <= ? \
                      UNION \
                      SELECT Spiel.SpielID, Team2ID TeamID, T2Tref Treffer, T1Tref Kassiert, \
                        Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet \
                        FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                        WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 \
                          AND Spiel.UnterwbID = ? AND Spieltag <= ?) AS t1 \
                    ON t2.TeamID = t1.TeamID \
                    GROUP BY t2.TeamID \
                    ORDER BY Punkte DESC, Differenz DESC, Treffer DESC, Team ASC;",
                    [leagueid, leagueid, matchday, leagueid, matchday])


def get_league_playertable(leagueid, matchday):
    return [dict(name=row[0], treffer=row[1], spiele=row[2], schnitt=round(float(row[1])/row[2], 2)) for row in
            query_db("SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = ls.SpielerID), \
                    SUM(treffer) AS Treffer, \
                    COUNT(*) AS Spiele \
                    FROM (Ligaspieler ls LEFT JOIN Spiel s ON ls.SpielID = s.SpielID) \
                    LEFT JOIN Ligaspiel lsp ON lsp.SpielID = s.SpielID \
                    WHERE s.UnterwbID = ? AND lsp.Spieltag <= ? \
                    GROUP BY ls.SpielerID ORDER BY treffer DESC, Spiele ASC", [leagueid, matchday])]


def get_league_matchday_max(leagueid):
    return query_db('SELECT MAX(Spieltag) \
                    FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                    WHERE UnterwbID = ?', [leagueid], one=True)


def get_league_matchday_current(leagueid):
    maxst = get_league_matchday_max(leagueid)
    while maxst != 1:
        if query_db('SELECT SiegerID \
                    FROM Spiel Inner Join Ligaspiel ON Spiel.SpielID = Ligaspiel.SpielID \
                    WHERE Spieltag = ? AND UnterwbID = ? AND SiegerID not null',
                    [maxst, leagueid], one=True):
            return maxst
        maxst -= 1
    return 1


def get_league_game_result(gameid):
    check_gamemode(gameid, 'liga')
    gametuple = query_db("SELECT Spiel.SpielID, \
                         (SELECT CASE WHEN T1Tref = 6 THEN CASE WHEN T2Tref = 5 THEN 'OTS' ELSE 'G' END \
                           ELSE CASE WHEN T1Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg1, \
                         (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID) AS T1, \
                         T1Tref, T2Tref, \
                         (SELECT Name From Team WHERE Team.TeamID = Spiel.Team2ID) AS T2, \
                         (SELECT CASE WHEN T2Tref = 6 THEN CASE WHEN T1Tref = 5 THEN 'OTS' ELSE 'G' END \
                           ELSE CASE WHEN T2Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg2, \
                         Ligaspiel.Spieltag \
                         FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SpielID = ? ",
                         [gameid])[0]
    spielerlist = []
    for spieler in query_db('SELECT \
                            (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Ligaspieler.SpielerID), \
                            Treffer FROM Ligaspieler WHERE SpielID = ? ', [gameid]):
        spielerlist.append(spieler)
    gametuple = gametuple + (spielerlist, )
    return gametuple


def get_group_game_result(gameid):
    check_gamemode(gameid, 'turnier')
    return query_db('SELECT Spiel.SpielID, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID), \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team2ID), \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.SiegerID), \
                    Becherueber \
                    FROM Spiel Inner Join Turnierspiel ON Spiel.SpielID = Turnierspiel.SpielID \
                    WHERE Spiel.SpielID = ?', [gameid])[0]


def get_ko_game_result(gameid):
    check_gamemode(gameid, 'ko')
    return query_db('SELECT Spiel.SpielID, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID), \
                    T1Erg, \
                    T2Erg, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team2ID) \
                    FROM Spiel Inner Join KOspiel ON Spiel.SpielID = KOspiel.SpielID \
                    WHERE Spiel.SpielID = ?', [gameid])[0]


def get_game_result(gameid):
    modus = query_db('SELECT (SELECT Modus FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID) \
                     FROM Spiel Where SpielID = ?', [gameid], one=True)
    if modus == 'liga':
        return get_league_game_result(gameid)
    elif modus == 'turnier':
        return get_group_game_result(gameid)
    else:  # modus == 'ko'
        return get_ko_game_result(gameid)


def get_game_data(gameid):
    return query_db('SELECT s.SpielID, s.UnterwbID, \
                    uwb.name, uwb.modus, \
                    Datum, Gewertet \
                    FROM Spiel s Inner Join Unterwettbewerb uwb On s.UnterwbID = uwb.UnterwbID \
                    WHERE SpielID = ?',
                    [gameid])[0]


def get_game_show_edit(gameid):
    players = []
    div_id = get_game_data(gameid)[1]

    team_ids = query_db("SELECT Team1ID, Team2ID FROM Spiel WHERE SpielID = ?", [gameid])[0]

    for row in query_db("SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Teilgenommen.SpielerID) FROM Teilgenommen WHERE UnterwbID = ? AND (TeamID = ? OR TeamID = ?)",
                        [div_id, team_ids[0], team_ids[1]]):
        players.append(row[0])

    if session.get('username') != 'mod' and session.get('username') not in players:
        return False

    phase = query_db("SELECT (SELECT Phase FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID) FROM Unterwettbewerb WHERE UnterwbID = ?", [div_id], one=True)
    if phase != 'laeuft':
        return False

    if session.get('username') == current_app.config['MODLOGIN']:
        return True

    if query_db("SELECT SiegerID FROM Spiel WHERE SpielID = ?", [gameid], one=True):
        return False

    return True

# ----------------------------------------------------------------------------------------------------------------------
#
# MOD Functions
#
# ----------------------------------------------------------------------------------------------------------------------


def get_registration_division(competitionid):
    return query_db('SELECT UnterwbID FROM Unterwettbewerb WHERE WbID = ?', [competitionid], one=True)


def get_player_registration(nickname, competitionid):
    divisionid = get_registration_division(competitionid)
    return query_db('SELECT \
                    (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) \
                    FROM Teilgenommen tg \
                    WHERE tg.SpielerID = (SELECT SpielerID FROM Spieler WHERE Nickname = ?) AND UnterwbID = ?',
                    [nickname, divisionid], one=True)


def register_player(nickname, divisionid, teamname):
    if get_player_registration(nickname, divisionid):
        flash('Spieler nicht angemeldet')
        flash('Spieler bereits fuer Unterwettbewerb registriert')
        return False
    playerid = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [nickname], one=True)
    teamid = query_db('SELECT TeamID FROM Team WHERE name = ?', [teamname], one=True)
    update_db('INSERT INTO Teilgenommen(UnterwbID, SpielerID, TeamID) VALUES (?, ?, ?)', [divisionid, playerid, teamid])
    competitionid = query_db('SELECT WbID FROM Unterwettbewerb WHERE UnterwbID = ?', [divisionid], one=True)
    if not get_player_registration(nickname, competitionid):
        flash('Spieler nicht angemeldet')
        flash('Fehler in Datenbankanfrage')
        return False
    flash('Spieler %s angemeldet' % nickname)
    flash('Team: %s' % teamname)
    return True


def unregister_player(nickname, competitionid):
    divisionid = get_registration_division(competitionid)
    if not get_player_registration(nickname, competitionid):
        flash('Spieler nicht abgemeldet')
        flash('Spieler war nicht eingetragen')
        return False
    playerid = query_db('SELECT SpielerID FROM Spieler WHERE Nickname = ?', [nickname], one=True)
    update_db('DELETE FROM Teilgenommen WHERE UnterwbID = ? AND SpielerID = ?', [divisionid, playerid])
    if get_player_registration(nickname, competitionid):
        flash('Spieler nicht abgemeldet')
        flash('Fehler in Datenbankabfrage')
        return False
    return True