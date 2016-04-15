from flask import current_app
from functions_general import query_db
from hashlib import sha1


def validate_password(nickname, password):
    fetchpass = query_db('SELECT Passwort FROM Spieler WHERE Nickname = ?', [nickname], one=True)
    if sha1(password+current_app.config['SALT']).hexdigest() == fetchpass or \
            (nickname == current_app.config['ADMINLOGIN'] and password == current_app.config['ADMINPASSWORD']) or \
            (nickname == current_app.config['MODLOGIN'] and password == current_app.config['ADMINPASSWORD']):
        return True
    else:
        return False
