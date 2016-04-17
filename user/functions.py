from flask import abort
from functions_general import query_db
from competition.functions import get_league_teamtable, get_league_matchday_current


def check_player(playername):
    if not query_db('SELECT * FROM Spieler WHERE Nickname = ?', [playername], one=True):
        return abort(404, 'Spieler existiert nicht')
    return


def check_team(teamname):
    if not query_db('SELECT * FROM Team WHERE Name = ?', [teamname], one=True):
        return abort(404, 'Team existiert nicht')
    return


def get_player_data(playername):
    check_player(playername)
    return query_db('SELECT SpielerID, Nickname, Vorname, Name FROM Spieler WHERE Nickname = ?', [playername])[0]


def get_player_history(playername):
    check_player(playername)
    history = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name, \
                        (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE SpielerID = (SELECT SpielerID FROM Spieler WHERE nickname = ?)', [playername]):
        divisionid = row[0]
        divisionname = row[2]
        team = row[3]
        if row[1] == 'liga':
            rank = get_league_teamrank(divisionid, team)
        else:
            # row[1] == 'ko'
            rank = 'Platzierung fuer KO nicht implementiert'
        line = (divisionid, divisionname, rank, team)
        history.append(line)
    return history


def get_team_data(teamname):
    check_team(teamname)
    return query_db('SELECT TeamID, Name FROM Team WHERE Name = ?', [teamname])[0]


def get_team_history(teamname):
    check_team(teamname)
    history = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE TeamID = (SELECT TeamID FROM Team WHERE name = ?)', [teamname]):
        divisionid = row[0]
        divisionname = row[2]
        if row[1] == 'liga':
            rank = get_league_teamrank(divisionid, teamname)
        else:
            # row[1] == 'ko'
            rank = 'Platzierung fuer KO nicht implementiert'
        spieler = query_db('SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Teilgenommen.SpielerID) \
                           FROM Teilgenommen \
                           WHERE UnterwbID = ? AND \
                           (SELECT name FROM Team WHERE Team.TeamID = Teilgenommen.TeamID) = ?', [divisionid, teamname])
        line = (divisionid, divisionname, rank, spieler)
        history.append(line)
    return history


def get_league_teamrank(leagueid, team):
    i = 1
    for item in get_league_teamtable(leagueid, get_league_matchday_current(leagueid)):
        if item[0] == team:
            return i
        i += 1
    return 0
