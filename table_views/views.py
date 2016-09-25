from flask import Blueprint, render_template, abort
from decorators import login_required
from functions_general import query_db


table_views = Blueprint('table_views', __name__, template_folder='templates')


# allowed for view:
# player, team, game, competition, division, participated
@table_views.route('/view/<view>')
@login_required(user='admin')
def views(view):
    return render_template('table_views/main.html', view=view, table=get_admin_table(view),
                           page_title='Tabelle: %s' % view)


def get_admin_table(view):
    if view == 'player':
        return [('ID', 'Nickname', 'Name', 'Vorname', 'Passworthash', 'Team')] + \
               query_db('SELECT SpielerID, Nickname, Name, Vorname, Passwort, \
                        (SELECT Name FROM Team WHERE Team.TeamID = Spieler.TeamID) \
                        FROM Spieler')
    elif view == 'team':
        return [('ID', 'Name', 'Spieler')] + \
               [row + ([item[0] for item in query_db('SELECT Nickname FROM Spieler WHERE TeamID = ?', [row[0]])], )
                for row in query_db('SELECT TeamID, Name FROM Team')]
    elif view == 'game_league':
        return [('ID', 'Unterwb', 'Team1', 'Team2', 'Sieger', 'Gewertet', 'Datum', 'Spieltag', 'T1Tref', 'T2Tref')] + \
               query_db('SELECT s.SpielID, \
                        (SELECT Name FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = s.UnterwbID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.Team1ID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.Team2ID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.SiegerID), \
                        Gewertet, \
                        Datum, \
                        Spieltag, \
                        T1Tref, \
                        T2Tref \
                        FROM Spiel s Inner Join Ligaspiel ON s.SpielID = Ligaspiel.SpielID')
    elif view == 'game_ko':
        return [('ID', 'Unterwb', 'Team1', 'Team2', 'Sieger', 'Gewertet', 'Datum',
                 'NFWin', 'NFLos', 'Bestof', 'T1Erg', 'T2Erg')] + \
               query_db('SELECT s.SpielID, \
                        (SELECT Name FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = s.UnterwbID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.Team1ID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.Team2ID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.SiegerID), \
                        Gewertet, \
                        Datum, \
                        NFWinnerID, \
                        NFLoserID, \
                        Bestofwhat, \
                        T1Erg,  \
                        T2Erg \
                        FROM Spiel s Inner Join KOspiel ON s.SpielID = KOspiel.SpielID')
    elif view == 'game_group':
        return [('ID', 'Unterwb', 'Team1', 'Team2', 'Sieger', 'Gewertet', 'Datum',
                 'Becherueber')] + \
               query_db('SELECT s.SpielID, \
                        (SELECT Name FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = s.UnterwbID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.Team1ID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.Team2ID), \
                        (SELECT Name FROM Team WHERE Team.TeamID = s.SiegerID), \
                        Gewertet, \
                        Datum, \
                        Becherueber \
                        FROM Spiel s Inner Join Turnierspiel ON s.SpielID = Turnierspiel.SpielID')
    elif view == 'competition':
        return [('WbID', 'Name')] + query_db('SELECT * FROM Wettbewerb')
    elif view == 'division':
        return [('ID', 'Wettbewerb', 'Name', 'Modus', 'OTN', 'Start', 'Ende')] + \
               query_db('SELECT UnterwbID, \
                        (SELECT Name FROM Wettbewerb WHERE Wettbewerb.WbID = Unterwettbewerb.WbID), \
                        Name, Modus, OTN, Unterwettbewerb.start, Ende \
                        FROM Unterwettbewerb')
    elif view == 'participated':
        return [('Unterwettbewerb', 'Team', 'Spieler')] + \
               query_db('SELECT \
                        (SELECT Name FROM Unterwettbewerb WHERE UnterwbID = tg.UnterwbID), \
                        (SELECT Name FROM Team WHERE TeamID = tg.TeamID), \
                        (SELECT Nickname FROM Spieler WHERE SpielerID = tg.SpielerID) \
                        FROM Teilgenommen tg')
    else:
        return abort(500, 'Error in admin.functions get_table error')
