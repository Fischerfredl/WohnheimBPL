# PC:
DATABASE = 'database.db'
# Laptop:
# DATABASE = 'C:\\Users\\alfre\\Documents\\GitHub\\WohnheimBPL\\database.db'
DEBUG = True
SECRET_KEY = 'initialKey'
SALT = 'initialSalt'
IPADDR = '0.0.0.0'
PORT = 5000


# acc for administrator
ADMINLOGIN = 'admin'
ADMINPASSWORD = 'initialPassword'

# acc for tournament mods
MODLOGIN = 'mod'
MODPASSWORD = 'initialPassword'

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
    'competition_reset': [MODLOGIN],
    'competition_delete': [MODLOGIN],
    'competition_player_assign': [MODLOGIN],
    'competition_player_unassign': [MODLOGIN],
    'player_assign_team': [MODLOGIN],
    'game_edit': [MODLOGIN, 'signed_user'],
    'sql_query': [ADMINLOGIN],
    'set_adminpassword': [ADMINLOGIN],
    'set_modpassword': [ADMINLOGIN],
    'set_secret_key': [ADMINLOGIN],
    'set_salt': [ADMINLOGIN],
    'division_rename': [MODLOGIN]
    }
