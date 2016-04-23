from flask import Blueprint, render_template, request
from decorators import settings_permission_required
from functions import *

settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/')
def home():
    return render_template('settings/settings.html', header=get_header(), options=get)


@settings.route('/<option>', methods=['GET', 'POST'])
@settings_permission_required
def main(option):
    if request.method == 'POST':
        if option == 'new_player':
            new_player()
        elif option == 'del_player':
            del_player()
        elif option == 'del_team':
            del_team()
        elif option == 'create_competition':
            create_competition()
        elif option == 'make_competition':
            make_competition()
        elif option == 'advance_competition':
            advance_competition()
        elif option == 'close_competition':
            close_competition()
        elif option == 'reopen_competition':
            reopen_competition()
        elif option == 'delete_competition':
            delete_competition()
        elif option == 'player_assign_team':
            player_assign_team()
        elif option == 'edit_game':
            edit_game()
        elif option == 'edit_player':
            edit_player()
        elif option == 'edit_player_reset_password':
            edit_player_reset_password()
        elif option == 'edit_player_set_password':
            edit_player_set_password()
        elif option == 'edit_team':
            edit_team()
    return render_template('settings/forms.html', option=option, header=get_header(), form=get_form(option))
