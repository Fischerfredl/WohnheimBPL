from flask import flash
from functions_general import get_new_id, get_competitions, update_db


def new_competition(name):
    if name in get_competitions():
        flash('Wettbewerb nicht erzeugt')
        flash('Name bereits vorhanden')
        return False
    competition_id = get_new_id('competition')
    update_db('INSERT INTO Wettbewerb(WbID, Name) VALUES (?, ?)', [competition_id, name])
    flash('Wettbewerb %s angelegt' % name)
    division_id = get_new_id('division')
    division_name = name + ' - Anmeldung'
    update_db("INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN) VALUES (?, ?, ?, 'anmeldung', 'ein')",
              [division_id, competition_id, division_name])
    flash('Unterwettbewerb %s angelegt' % division_name)
    return True
