from flask import Blueprint, render_template, url_for, redirect, request
from decorators import login_required
from functions import *

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/')
@login_required(user='admin')
def home():
    return render_template('admin/admin.html')


# allowed for option:
# new_player, new_team, new_password, del_player, del_team
@admin.route('/settings/<option>', methods=['GET', 'POST'])
@login_required(user='admin')
def settings(option):
    if request.method == 'POST':
        if option == 'new_player':
            new_player(request.form['nickname'], request.form['name'], request.form['vorname'])
        elif option == 'new_team':
            new_team(request.form['name'])
        elif option == 'del_player':
            del_player(request.form['nickname'])
        elif option == 'del_team':
            del_team(request.form['name'])
        elif option == 'new_password':  # option == 'resetpw'
            new_password(request.form['nickname'])
        else:
            abort(404, 'Einstellungen gibbet nich')
        return redirect(url_for('admin.home'))
    else:  # request.method == 'GET'
        return render_template('admin/admin_settings.html', option=option, itemlist=get_items(option))


