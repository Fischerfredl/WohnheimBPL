DATABASE = 'D:\\Dateien\\Dokumente\\GitHub\\WohnheimBPL\\database.db'
DEBUG = True
SECRET_KEY = '=R(Db4%ijH3GZd)1cmirMy7sP(%V95=h'
SALT = 'salt!!!#22*'
IPADDR = '0.0.0.0'
PORT = 5000


# acc for administrator
ADMINLOGIN = 'admin'
ADMINPASSWORD = 'password'

# acc for tournament mods
MODLOGIN = 'mod'
MODPASSWORD = 'password'

# Settings {option: permissions}
SETTINGS = {
    'new_player': [ADMINLOGIN, MODLOGIN],
    'new_team': [ADMINLOGIN, MODLOGIN, 'signed_user'],
    'del_player': [ADMINLOGIN, MODLOGIN],
    'del_team': [ADMINLOGIN, MODLOGIN],
    'create_competition': [MODLOGIN],
    'make_competition': [MODLOGIN],
    'advance_competition': [MODLOGIN],
    'close_competition': [MODLOGIN],
    'reopen_competition': [MODLOGIN],
    'delete_competition': [MODLOGIN],
    'player_assign_team': [MODLOGIN],
    'edit_game': [MODLOGIN, 'signed_user'],
    'edit_player': [ADMINLOGIN, MODLOGIN, 'signed_user'],
    'edit_player_reset_password': [ADMINLOGIN, MODLOGIN],
    'edit_player_set_password': [ADMINLOGIN, MODLOGIN, 'signed_user'],
    'edit_team': [ADMINLOGIN, MODLOGIN, 'signed_user']
    }
