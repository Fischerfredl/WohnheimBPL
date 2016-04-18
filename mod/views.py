from flask import Blueprint, render_template, request, redirect, url_for, abort
from decorators import login_mod_required
from functions import *


mod = Blueprint('mod', __name__, template_folder='templates')

@mod.route('/')
@login_mod_required
def home():
    return render_template('mod/mod.html')


# allowed for option:
# new_player, new_team, new_password, del_player, del_team
@mod.route('/settings/<option>', methods=['GET', 'POST'])
@login_mod_required
def settings(option):
    if request.method == 'POST':
        if option == 'new_competition':
            new_competition(request.form['name'])
        else:
            abort(404, 'Einstellungen gibbet nich')
        return redirect(url_for('mod.home'))
    else:  # request.method == 'GET'
        return render_template('mod/mod_settings.html', option=option)
