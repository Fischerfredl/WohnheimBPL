from flask import Blueprint, render_template, redirect, url_for, request, session
from functions import *
from functions_general import get_teams
from decorators import login_required, \
    check_game, check_competition, check_division, check_league,  check_league_matchday, \
    check_competition_phase, check_player

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
    anmeldung = query_db("SELECT WbID, Name From Wettbewerb WHERE Phase = 'anmeldung'")
    return render_template('competition/competition_overview.html', competition_overview=get_competition_overview(), anmeldung=anmeldung,
                           page_title='Home')


@competition.route('/<int:competitionid>')
@check_competition
def detail_competition(competitionid):
    return render_template('competition/competition.html', object=get_competition_info(competitionid),
                           table_divisions=get_competition_divisions(competitionid),
                           page_title='Wettberwerb %s' % get_competition_info(competitionid)[1])


@competition.route('/division/<int:divisionid>')
@check_division
def detail_division(divisionid):
    modus = get_division_mode(divisionid)
    if modus == 'liga':
        return redirect(url_for('competition.detail_league',
                                leagueid=divisionid, matchday=get_league_matchday_current(divisionid)))
    elif modus == 'turnier':
        return render_template('competition/detail_group.html', object=get_division_info(divisionid),
                               table_spiele=get_group_games_info(divisionid),
                               page_title='Turnier: %s' % get_division_info(divisionid)[1])
    elif modus == 'ko':
        return render_template('competition/detail_ko.html', object=get_division_info(divisionid),
                               table_spiele=get_ko_games_info(divisionid),
                               page_title='KO-Runde: %s' % get_division_info(divisionid)[1])
    else:  # modus = 'anmeldung'
        return render_template('competition/register.html', object=get_division_info(divisionid),
                               page_title='Anmeldung: %s' % get_division_info(divisionid)[1])


@competition.route('/division/<int:leagueid>/<int:matchday>')
@check_league
@check_league_matchday
def detail_league(leagueid, matchday):
    table_teamtable = get_league_teamtable(leagueid, matchday)
    table_playertable = get_league_playertable(leagueid, matchday)
    table_playertable_small = []
    count = 0
    if table_playertable:
        while count < len(table_teamtable):
            if count < len(table_playertable):
                table_playertable_small.append(table_playertable[count])
            count += 1
    return render_template('competition/detail_league.html', object=get_division_info(leagueid),
                           matchday=matchday, matchday_max=get_league_matchday_max(leagueid),
                           table_teamtable=table_teamtable,
                           table_playertable=table_playertable,
                           table_playertable_small=table_playertable_small,
                           table_games=get_league_games_info(leagueid, matchday),
                           page_title='Liga: %s' % get_division_info(leagueid)[1])

@competition.route('/division/<int:leagueid>/<int:matchday>/fullscreen')
@check_league
@check_league_matchday
def detail_league_fullscreen(leagueid, matchday):
    table_teamtable = get_league_teamtable(leagueid, matchday)
    table_playertable = get_league_playertable(leagueid, matchday)
    return render_template('competition/detail_league_fullscreen.html', object=get_division_info(leagueid),
                           matchday=matchday, matchday_max=get_league_matchday_max(leagueid),
                           table_teamtable=table_teamtable,
                           table_playertable=table_playertable,
                           table_games=get_league_games_info(leagueid, matchday),
                           large=1,
                           page_title='Liga: %s' % get_division_info(leagueid)[1])


@competition.route('/<int:competitionid>/teams')
@check_competition
def competition_signed_teams(competitionid):
    return render_template('competition/competition_signed_teams.html', object=get_competition_info(competitionid),
                           signed_teams=get_competition_teams(competitionid),
                           page_title='Teams: %s' % get_competition_info(competitionid)[1])


@competition.route('/division/<int:divisionid>/teams')
@check_division
def division_signed_teams(divisionid):
    return render_template('competition/competition_signed_teams.html', object=get_division_info(divisionid),
                           signed_teams=get_division_teams(divisionid),
                           page_title='Teams: %s' % get_division_info(divisionid)[1])


@competition.route('/game/<int:gameid>')
@check_game
def detail_game(gameid):
    session['gameid'] = gameid
    return render_template('competition/detail_game.html', result=get_game_result(gameid), data=get_game_data(gameid),
                           show_edit=get_game_show_edit(gameid),
                           page_title='Spiel-Nr %i' % gameid)


@competition.route('/register_player/<int:competitionid>/<nickname>/', methods=['GET', 'POST'])
@check_player
@login_required(user='designated')
@check_competition
@check_competition_phase('anmeldung')
def register(competitionid, nickname):
    if request.method == 'POST':
        division = get_registration_division(competitionid)
        register_player(nickname, division, request.form['name'])
        return redirect(url_for('competition.detail_competition', competitionid=competitionid))
    else:  # method = 'GET'
        return render_template('competition/register.html', object=get_competition_info(competitionid),
                               registration=get_player_registration(nickname, competitionid),
                               teamlist=get_teams(),
                               page_title='Anmeldung: %s' % get_competition_info(competitionid)[1])


@competition.route('/unregister_player/<int:competitionid>/<nickname>/')
@check_player
@login_required(user='designated')
@check_competition
@check_competition_phase('anmeldung')
def unregister(competitionid, nickname):
    unregister_player(nickname, competitionid)
    return redirect(url_for('competition.detail_competition', competitionid=competitionid))


@competition.route('/legend')
def legend():
    return render_template('competition/legend.html', page_title='Legende')
