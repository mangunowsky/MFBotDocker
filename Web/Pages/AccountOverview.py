import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event, Input, State

from app import app
from Functions import globalVariables, AccountFun, SettingsFun, LogFun
from Utils import ComUtils, HTMLUtils, logUtil

cache = ""


def getLayout():
    global cache
    if cache == "":
        cache = [
            html.H2("Account Overview"),
            html.H3("Perform action on all accounts"),
            html.Table(id="action_table", children=[
                html.Tr([
                    html.Td(html.Button('Login', id="bAccs_Perform_Login", type="submit")),
                    html.Td(html.Button('Logout', id="bAccs_Perform_Logout", type="submit")),
                    html.Td(html.Button('Start', id="bAccs_Perform_Start", type="submit")),
                    html.Td(html.Button('Stop', id="bAccs_Perform_Stop", type="submit")),
                    html.Td(html.Button('Stop Current Action', id="bAccs_Perform_Cancel", type="submit")),
                    ])
                ]),
            html.H3("Select Table columns"),
            dcc.Dropdown(options=getColums(), value=getColumDefaults(),
                         multi=True, id="iColumSelection"),
            html.Div(id='accounts_Overview', children=[]),
            dcc.Interval(id='accounts_interval',
                         interval=globalVariables.WEBSITE_REFRESH_RATE, n_intervals=0)
            ]
    return cache


def getColums():
    return[{'label': a["label"], 'value':a["value"]} for a in globalVariables.columNames]


def getColumDefaults():
    arr = []
    for a in globalVariables.columNames:
        if a["default"]:
            arr.append(a["value"])
    return arr


def initCallbacks():
    @app.callback(Output('AccsAction1', 'children'),
                  [],[],
                  # [Input('bAccount', 'n_clicks')],
                  [Event('bAccs_Perform_Login', 'click')])
    def cb_AccountsAction_Login():
        logUtil.log(2, "Performing !Login on All Accounts")
        for a in globalVariables.account_names:
            ComUtils.curlGet("bot/accounts/"+a+"!Login")
        logUtil.log(2, "All accounts should be logged in now")
        return []
    @app.callback(Output('AccsAction2', 'children'),
                  [],[],
                  # [Input('bAccount', 'n_clicks')],
                  [Event('bAccs_Perform_Logout', 'click')])
    def cb_AccountsAction_Logout(action):
        logUtil.log(2, "Performing !Logout on All Accounts")
        for a in globalVariables.account_names:
            ComUtils.curlGet("bot/accounts/"+a+"!Logout")
        logUtil.log(2, "All accounts should be logged out now")
        return []
    @app.callback(Output('AccsAction3', 'children'),
                  [],[],
                  # [Input('bAccount', 'n_clicks')],
                  [Event('bAccs_Perform_Start', 'click')])
    def cb_AccountsAction_Start():
        logUtil.log(2, "Performing !Start on All Accounts")
        for a in globalVariables.account_names:
            ComUtils.curlGet("bot/accounts/"+a+"!Start")
        logUtil.log(2, "All accounts should be started now")
        return []
    @app.callback(Output('AccsAction4', 'children'),
                  [],[],
                  # [Input('bAccount', 'n_clicks')],
                  [Event('bAccs_Perform_Stop', 'click')])
    def cb_AccountsAction_Stop():
        logUtil.log(2, "Performing !Stop on All Accounts")
        for a in globalVariables.account_names:
            ComUtils.curlGet("bot/accounts/"+a+"!Stop")
        logUtil.log(2, "All accounts should be stopped now")
        return []
    @app.callback(Output('AccsAction5', 'children'),
                  [],[],
                  # [Input('bAccount', 'n_clicks')],
                  [Event('bAccs_Perform_Cancel', 'click')])
    def cb_AccountsAction_Cancel():
        logUtil.log(2, "Performing !StopCurrentAction on All Accounts")
        for a in globalVariables.account_names:
            ComUtils.curlGet("bot/accounts/"+a+"!StopCurrentAction")
        logUtil.log(2, "All accounts should´ve stopped current action now")
        return []
    @app.callback(Output('accounts_Overview', 'children'),
                  [Input('accounts_interval', 'n_intervals')],
                  # [Input('bAccount', 'n_clicks')],
                  [State('iColumSelection', 'value')])
    def cb_Accounts(n, pSelect):
        return AccountFun.getAccounts(pSelect)
