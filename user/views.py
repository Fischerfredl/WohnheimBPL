from flask import Blueprint, render_template
from functions import *


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/user/<nickname>')
def detailplayer(nickname):
    return render_template('detail_player.html', data=get_player_data(nickname), history=get_player_history(nickname))


@user.route('/team/<teamname>')
def detailteam(teamname):
    return render_template('detail_team.html', data=get_team_data(teamname), history=get_team_history(teamname))
