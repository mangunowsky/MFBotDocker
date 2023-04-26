from datetime import datetime, timedelta


def init():
    global VALID_USERNAME_PASSWORD_WEB_INTERFACE, USERNAME, PASSWORD, ADRESS, serverPort, REFRESH_RATE_ALL_DATA, WEBSITE_REFRESH_RATE
    global settings, ACCOUNTS_o, SETTING_LIST, ACC_SETTING_LIST, settings_send, account_Setting_Send, LIGHT, settingsChanges, logs, accounts, account_names
    global callbackList, CACHE_ACCS, GLOBAL_SETTINGS_lastRequest, CACHE_BOT_LOG, accLast, noSlider, accountOptions, columNames, columHeaders
    global debugLevel, debugLevels, debugColors
    VALID_USERNAME_PASSWORD_WEB_INTERFACE = [
        ['Entwickler', 'MFBot5.0']
        ]
    USERNAME = "admin"
    PASSWORD = "admin"
    ADRESS = 'http://127.0.0.1:6969/'
    serverPort = 8050

    # Time in s after wich new Data should be requested from Remote Interface
    REFRESH_RATE_ALL_DATA = 5
    # Time in ms after wich the website shall request new Data
    WEBSITE_REFRESH_RATE = 10*1000

    LIGHT = False
    settings = {}
    ACCOUNTS_o = {}
    SETTING_LIST = []
    ACC_SETTING_LIST = []
    settings_send = {}
    account_Setting_Send = {}
    settingsChanges = False
    logs = []
    accounts = []
    account_names = []
    callbackList = []

    CACHE_ACCS = {"lastRequest": datetime.now() - timedelta(minutes=15),
                  "data": [], "newData": True}
    GLOBAL_SETTINGS_lastRequest = datetime.now() - timedelta(minutes=15)
    CACHE_BOT_LOG = {"lastRequest": datetime.now() - timedelta(minutes=15),
                     "data": [], "newData": True, "amount": 10, "maxTime": datetime.now()}

    accLast = ""
    noSlider = False
    accountOptions = [
        {'label': 'Login', 'value': '!Login'},
        {'label': 'Logout', 'value': '!Logout'},
        {'label': 'Start', 'value': '!Start'},
        {'label': 'Stop', 'value': '!Stop'},
        {'label': 'Stop Current Action', 'value': '!StopCurrentAction'}
        ]
    columNames = [
        {'label': 'ALU', 'value': 'aLU', 'default': True, 'type': ''},
        {'label': 'Logged In?', 'value': 'isLoggedIn', 'default': True, 'type': ''},
        {'label': 'Running?', 'value': 'isStarted', 'default': True, 'type': ''},
        {'label': 'Current Action', 'value': 'currentAction',
            'default': True, 'type': ''},
        {'label': 'Busy Until', 'value': 'busyUntil',
            'default': True, 'type': 'time'},
        {'label': 'Beer', 'value': 'usedBeer', 'default': True, 'type': 'beer'},
        {'label': 'Level', 'value': 'level', 'default': True, 'type': ''},
        {'label': 'Guild', 'value': 'guildName', 'default': False, 'type': ''},
        {'label': 'Class', 'value': 'class', 'default': False, 'type': ''},
        {'label': 'Gold', 'value': 'gold', 'default': True, 'type': ''},
        {'label': 'Shrooms', 'value': 'mushrooms', 'default': True, 'type': ''},
        {'label': 'Portal?', 'value': 'portalFought', 'default': False, 'type': ''},
        {'label': 'Dungeon Timer', 'value': 'dungeonTimer',
            'default': False, 'type': 'time'},
        {'label': 'Honor', 'value': 'honor', 'default': False, 'type': ''},
        {'label': 'Rank', 'value': 'rank', 'default': True, 'type': ''},
        {'label': 'XP', 'value': 'experience', 'default': True, 'type': ''},
        {'label': 'XP Needed', 'value': 'experienceForNextLevel',
            'default': False, 'type': ''},
        {'label': 'XP %', 'value': 'experienceInPercent',
            'default': True, 'type': 'percent'},
        {'label': 'Mount Speed', 'value': 'mountSpeed', 'default': False, 'type': ''},
        {'label': 'Mount Until', 'value': 'mountEnd',
            'default': False, 'type': 'time'},
        {'label': 'Mirror?', 'value': 'hasMirror', 'default': False, 'type': ''},
        {'label': 'Mirror Pieces', 'value': 'mirrorProgress',
            'default': False, 'type': ''},
        {'label': 'SA %', 'value': 'albumProgress',
            'default': True, 'type': 'percent'},
        {'label': 'Arena XP', 'value': 'arenaXP', 'default': False, 'type': ''},
        {'label': 'Aura', 'value': 'aura', 'default': False, 'type': ''}
        ]
    columHeaders = {}
    for a in columNames:
        columHeaders[a["value"]] = {'label': a["label"], 'type': a["type"]}
    debugLevel = 3
    debugLevels = ["Special Debug","Debug","Info","Warnings","Errors"]
    debugColors = ['\033[34m','\033[90m','\033[32m','\033[33;1m','\033[31m']
