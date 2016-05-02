from flask import Blueprint, render_template, request, redirect, url_for, abort
from decorators import login_required, check_competition, check_competition_phase
from functions import *


mod = Blueprint('mod', __name__, template_folder='templates')


# allowed for option:
# new_competition, del_competition
@mod.route('/settings/<option>', methods=['GET', 'POST'])
@login_required(user='mod')
def settings(option):
    if request.method == 'POST':
        if option == 'new_competition':
            new_competition(request.form['name'])
        elif option == 'del_competition':
            delete_competition(request.form['competitionid'])
        else:
            abort(404, 'Einstellungen gibbet nich')
        return redirect(url_for('mod.home'))
    else:  # request.method == 'GET'
        return render_template('mod/mod_settings.html', option=option, itemlist=get_items(option))


