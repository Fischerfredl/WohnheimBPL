from flask import Blueprint, render_template, request, abort
from decorators import settings_permission_required, login_required
from functions import *

settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/')
def home():
    return render_template('settings/settings.html', header=get_header(), options=get_options_by_permission(),
                           page_title='Einstellungen')


@settings.route('/<option>', methods=['GET', 'POST'])
@settings_permission_required
def main(option):
    if request.method == 'POST':
        if option == 'player_new':
            player_new()
        elif option == 'player_del':
            player_del()
        elif option == 'player_edit':
            player_edit()
        elif option == 'player_reset_password':
            player_reset_password()
        elif option == 'player_set_password':
            player_set_password()
        elif option == 'team_new':
            team_new()
        elif option == 'team_del':
            team_del()
        elif option == 'team_edit':
            team_edit()
        elif option == 'competition_create':
            competition_create()
        elif option == 'competition_make':
            competition_make()
        elif option == 'competition_advance':
            competition_advance()
        elif option == 'competition_close':
            competition_close()
        elif option == 'competition_reopen':
            competition_reopen()
        elif option == 'competition_reset':
            competition_reset()
        elif option == 'competition_delete':
            competition_delete()
        elif option == 'competition_player_assign':
            competition_player_assign()
        elif option == 'competition_player_unassign':
            competition_player_unassign()
        elif option == 'player_assign_team':
            player_assign_team()
        elif option == 'game_edit':
            game_edit()
        elif option == 'sql_query':
            sql_query()
        elif option == 'set_adminpassword':
            set_adminpassword()
        elif option == 'set_modpassword':
            set_modpassword()
        elif option == 'set_secret_key':
            set_secret_key()
        elif option == 'set_salt':
            set_salt()
        elif option == 'division_rename':
            division_rename()
        else:
            abort(404)

    form = get_form(option)
    hide_submit = 0
    for item in form:
        if item['type'] == 'select_list':
            if not item.get('value'):
                hide_submit = 1
        if item['label'] == 'Spiel bereits eingetragen':
            gameid = session.get('gameid')
            leagueid = query_db("SELECT UnterwbID FROM Spiel WHERE SpielID = ?", [gameid], one=True)
            matchday = query_db("SELECT Spieltag FROM Ligaspiel WHERE SpielID = ?", [gameid], one=True)
            return redirect(url_for('competition.detail_league', leagueid=leagueid, matchday=matchday))
    return render_template('settings/forms.html', option=option, header=get_header(), form=form,
                           hide_submit=hide_submit, page_title='Einstellungen: %s' % get_header()[option])


