DATABASE = 'D:\\Dateien\\Dokumente\\GitHub\\WohnheimBPL\\database.db'
DEBUG = True
SECRET_KEY = '=R(Db4%ijH3GZd)1cmirMy7sP(%V95=h'
SALT = 'salt!!!#22*'
IPADDR = '0.0.0.0'
PORT = 5000


# acc for administrator
ADMINLOGIN = 'admin'
ADMINPASSWORD = 'super-secure-password'

# acc for tournament mods
MODLOGIN = 'mod'
MODPASSWORD = 'super-secure-password'

# Settings {option: permissions}
SETTINGS = {
    'player_new': [ADMINLOGIN, MODLOGIN],
    'player_del': [ADMINLOGIN, MODLOGIN],
    'player_edit': ['signed_user'],
    'player_reset_password': [ADMINLOGIN, MODLOGIN],
    'player_set_password': ['signed_user'],
    'team_new': [ADMINLOGIN, MODLOGIN, 'signed_user'],
    'team_del': [ADMINLOGIN, MODLOGIN],
    'team_edit': ['signed_user'],
    'competition_create': [MODLOGIN],
    'competition_make': [MODLOGIN],
    'competition_advance': [MODLOGIN],
    'competition_close': [MODLOGIN],
    'competition_reopen': [MODLOGIN],
    'competition_delete': [MODLOGIN],
    'player_assign_team': [MODLOGIN],
    'game_edit': [MODLOGIN, 'signed_user']
    }
