from flask import Blueprint, render_template, request, redirect, url_for, abort
from decorators import login_required, check_team, check_player
from functions import *


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/user/<nickname>')
@check_player
def detail_player(nickname):
    return render_template('user/detail_player.html',
                           data=get_player_data(nickname), history=get_player_history(nickname))


@user.route('/team/<teamname>')
@check_team
def detail_team(teamname):
    return render_template('user/detail_team.html', data=get_team_data(teamname), history=get_team_history(teamname))


@user.route('/user/<nickname>/settings/<option>', methods=['GET', 'POST'])
@check_player
@login_required
def settings(nickname, option):
    if request.method == 'POST':
        if option == 'personal':
            new_personal_info(nickname, request.form['name'], request.form['vorname'])
        elif option == 'password':
            new_password(nickname, request.form['pwold'], request.form['pwnew'])
        elif option == 'nickname':
            if new_nickname(nickname, request.form['password'], request.form['nicknew']):
                return redirect(url_for('user.detail_player', nickname=request.form['nicknew']))
        else:
            abort(404, 'Einstellung gibbet nich')
        return redirect(url_for('user.detail_player', nickname=nickname))
    # else:  # request.method == 'GET'
    return render_template('user/user_settings.html', option=option, nickname=nickname)
