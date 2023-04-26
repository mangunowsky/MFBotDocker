import dash
import dash_auth
import traceback
from dash.dependencies import Output, Event, Input, State
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

# non-dash-related libraries
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import os
import json
import threading
import time
import flask
import sys
import getopt
from pprint import pprint

from Functions import globalVariables, SettingsFun

from Functions import AccountFun, LogFun
from Utils import HTMLUtils, ComUtils, logUtil

from Pages import AccountDetails, AccountSettings, BotLog, BotSettings, AccountOverview
from app import app, initServer


def initDetails():
    AccountFun.updateAccs(False)
    SettingsFun.getSettingsMeta()
    for name in globalVariables.account_names:
        SettingsFun.getSettingsMeta(name)
    details = ComUtils.curlGet()
    logUtil.log(0,details)
    try:
        globalVariables.logs = details["response"]["logs"]["logs"]
        globalVariables.accounts = details["response"]["bot"]["accounts"]
        successful = True
    except (KeyError):
        logUtil.log(4,"Key Error, remote Response: " + str(details))
        successful = False
    if successful:
        globalVariables.account_names = []
        for o in globalVariables.accounts:
            for key in o.keys():
                globalVariables.account_names.append(key)
                if not key in globalVariables.ACCOUNTS_o.keys():
                    globalVariables.ACCOUNTS_o[key] = AccountFun.Account(
                        key, o[key]["logs"]["logs"])
                SettingsFun.parseSettings(
                    o[key]["settings"]["settings"], key)
        try: #global settings
            aSettings = details["response"]["settings"]["settings"]
            SettingsFun.parseSettings(aSettings)
        except (KeyError):
            logUtil.log(4,"No global Settings in Response")

    logUtil.log(2,"Detected Accounts: " + str(globalVariables.account_names))
    # print(curlGet("loginErrors"))


def initHTML():
    initDetails()
    AccountOverview.initCallbacks()
    AccountDetails.initCallbacks()
    AccountSettings.initCallbacks()
    BotLog.initCallbacks()
    BotSettings.initCallbacks()

    @app.callback(Output('page_content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/Account':
            return AccountDetails.getLayout()
        elif pathname is not None and pathname.startswith('/Account/'):
            return AccountDetails.getLayout(pathname.split('/')[-1])
        elif pathname == '/Bot_Log':
            return BotLog.getLayout()
        elif pathname == '/Settings':
            return BotSettings.getLayout()
        elif pathname == '/AccountSettings':
            return AccountSettings.getLayout()
        else:
            return AccountOverview.getLayout()

    @app.callback(Output('sliderRadio', 'children'),
                  [Input('slider_Selection', 'value')])
    def cb_NoSlider(c):
        if c is not None:
            globalVariables.noSlider = False if c == "1" else True
        return html.P("")


def threadServer():
    app.run_server(host='0.0.0.0', port=globalVariables.serverPort)


def watchdog():
    tServer = threading.Thread(target=threadServer)
    tServer.daemon = False
    tServer.start()
    time.sleep(2)  # get Server start
    logUtil.log(2,"Server should be running now")
    tUpdater_Accs = threading.Thread(target=AccountFun.threadUpdateAccs)
    tUpdater_Accs.daemon = False
    tUpdater_Accs.start()
    logUtil.log(2,"Account Updater should be running now")
    tUpdater_Log = threading.Thread(target=LogFun.threadUpdateBotLog)
    tUpdater_Log.daemon = False
    tUpdater_Log.start()
    logUtil.log(2,"Bot Log Updater should be running now")
    tUpdater_ACCLog = threading.Thread(
        target=AccountFun.threadUpdateAccountLog)
    tUpdater_ACCLog.daemon = False
    tUpdater_ACCLog.start()
    logUtil.log(2,"Acc Log Updater should be running now")
    tUpdater_ACCSettings = threading.Thread(
        target=SettingsFun.threadUpdateSettings)
    tUpdater_ACCSettings.daemon = False
    tUpdater_ACCSettings.start()
    logUtil.log(2,"Acc Settings Updater should be running now")
    while True:
        time.sleep(2)
        alive = True
        if not tServer.isAlive():
            alive = False
            logUtil.log(4,"Watchdog detected dead Server, restarting")
            tServer = threading.Thread(target=threadServer)
            tServer.daemon = False
            tServer.start()
        if not tUpdater_Accs.isAlive():
            alive = False
            logUtil.log(4,"Watchdog detected dead Accounts Updater, restarting")
            tUpdater_Accs = threading.Thread(
                target=AccountFun.threadUpdateAccs)
            tUpdater_Accs.daemon = False
            tUpdater_Accs.start()
        if not tUpdater_Log.isAlive():
            alive = False
            tUpdater_Log = threading.Thread(
                target=LogFun.threadUpdateBotLog)
            tUpdater_Log.daemon = False
            tUpdater_Log.start()
            logUtil.log(4,"Watchdog detected dead Bot Log Updater, restarting")
        if not tUpdater_ACCLog.isAlive():
            alive = False
            tUpdater_ACCLog = threading.Thread(
                target=AccountFun.threadUpdateAccountLog)
            tUpdater_ACCLog.daemon = False
            tUpdater_ACCLog.start()
            logUtil.log(4,"Watchdog detected dead Acc Log Updater, restarting")
        if not tUpdater_ACCSettings.isAlive():
            alive = False
            tUpdater_ACCSettings = threading.Thread(
                target=SettingsFun.threadUpdateSettings)
            tUpdater_ACCSettings.daemon = False
            tUpdater_ACCSettings.start()
            logUtil.log(4,"Watchdog detected dead Acc Settings Updater, restarting")
        if not alive:
            logUtil.log(3,"Watchdog got some bad sheeps back to group")


def handleArgs(argv):
    try:
        opts, args = getopt.getopt(
            argv, "ha:p:d:", ["adress=", "port=","debug=","remoteU=", "remoteP=", "webU=", "webP=", "light-theme="])
    except getopt.GetoptError:
        print('MainProgram.py -h')
        sys.exit(2)
    wUser = ""
    wPass = ""
    for opt, arg in opts:
        if opt == '-h':
            print('test.py --port 8050 --remoteU "Username" --remoteP "Pa$$w0rd"')
            print("--remoteU specifies the desired User for Remote Interface Connection")
            print("--remoteP specifies the passowrd for Remote Interface Connection")
            print("--webU specifies the desired User for Web Interface Connection")
            print("--webP specifies the passowrd for Web Interface Connection")
            print("--adress specifies the Adress of the Remote Interface e.g. http://localhost:1024")
            print("--light-theme specifies whether the light design stylesheet is enabled instead of the dark one")
            sys.exit()
        elif opt in ("-p", "--port"):
            globalVariables.serverPort = int(arg)
        elif opt in ("-a", "--adress"):
            globalVariables.ADRESS = arg
        elif opt in ("-d", "--debug"):
            globalVariables.debugLevel = int(arg)
        elif opt in ("--remoteU"):
            globalVariables.USERNAME = arg
        elif opt in ("--remoteP"):
            globalVariables.PASSWORD = arg
        elif opt in ("--webU"):
            wUser = arg
        elif opt in ("--webP"):
            wPass = arg
        elif opt in ("--light-theme"):
            globalVariables.LIGHT = arg

    if (not wUser == "") and (not wPass == ""):
        globalVariables.VALID_USERNAME_PASSWORD_WEB_INTERFACE.append([
                                                                     wUser, wPass])
    auth = dash_auth.BasicAuth(
        app, globalVariables.VALID_USERNAME_PASSWORD_WEB_INTERFACE)
    logUtil.log(4,"Legend: This is an error message")
    logUtil.log(3,"Legend: This is a warning message")
    logUtil.log(2,"Legend: This is an info message")
    logUtil.log(1,"Legend: This is a debug message")
    logUtil.log(0,"Legend: This is a deep debug message")
    logUtil.log(1,'Remote Interface Adress is ' + globalVariables.ADRESS)
    logUtil.log(1,'Web Interface Port is ' + str(globalVariables.serverPort))
    logUtil.log(1,'Debug Level is ' + str(globalVariables.debugLevel))


if __name__ == '__main__':
    globalVariables.init()
    #"2018-06-11T18:15:05.909554+0200" .%f%z
    # dt_object = datetime.strptime("2018-06-11T18:15:05.909554+0200","%Y-%m-%dT%H:%M:%S.%f%z")
    handleArgs(sys.argv[1:])
    logUtil.log(1,"Starting server")
    initServer()
    logUtil.log(1,"Starting Initial Updating")
    initHTML()
    logUtil.log(1,"Initial Updating Done")
    watchdog()
