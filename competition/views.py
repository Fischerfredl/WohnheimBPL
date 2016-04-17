from flask import Blueprint, render_template, redirect, url_for
from functions import *

# /overview
# /<competitionid>
# /division/<divisionid>
# /division/<leagueidid>/<matchday>
# /<competitionid>/teams
# /division/<divisionid>/teams

# competition
# competition_overview.html
# competition_signed_teams.html
# detail_game.html
# detail_group
# detail_league.html
# detail_ko.html
# division.html
# division_signed_teams.html
# macros.html


competition = Blueprint('competition', __name__, template_folder='competition/templates')


@competition.route('/overview')
def overview():
    return render_template('competition_overview.html', competition_overview=get_competition_overview())


@competition.route('/<int:competitionid>')
def detail_competition(competitionid):
    return render_template('competition.html', object=get_competition_info(competitionid),
                           table_divisions=get_competition_divisions(competitionid))


@competition.route('/division/<int:divisionid>')
def division(divisionid):
    modus = get_division_mode(divisionid)
    if modus == 'liga':
        return redirect(url_for('competition.detail_league',
                                leagueid=divisionid, matchday=get_league_matchday_current(divisionid)))
    elif modus == 'turnier':
        return render_template('detail_group.html', object=get_division_info(divisionid),
                               table_spiele=get_group_games_info(divisionid))
    else:  # modus == 'ko'
        return render_template('detail_ko.html', object=get_division_info(divisionid),
                               table_spiele=get_ko_games_info(divisionid))


@competition.route('/division/<int:leagueid>/<int:matchday>')
def detail_league(leagueid, matchday):
    return render_template('detail_league.html', object=get_division_info(leagueid),
                           matchday=matchday, matchday_max=get_league_matchday_max(leagueid),
                           table_teamtable=get_league_teamtable(leagueid, matchday),
                           table_playertable=get_league_playertable(leagueid, matchday),
                           table_games=get_league_games_info(leagueid, matchday))


@competition.route('/competition/<int:competitionid>/teams')
def competition_signed_teams(competitionid):
    return render_template('competition_signed_teams.html', object=get_competition_info(competitionid),
                           signed_teams=get_competition_teams(competitionid))


@competition.route('/competition/division/<int:divisionid>/teams')
def division_signed_teams(divisionid):
    return render_template('competition_signed_teams.html', object=get_division_info(divisionid),
                           signed_teams=get_division_teams(divisionid))


@competition.route('/game/<int:gameid>')
def detailgame(gameid):
    return render_template('detail_game.html', result=get_game_result(gameid), data=get_game_data(gameid))
