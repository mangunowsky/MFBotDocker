import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event, Input, State

from app import app
from Functions import globalVariables, AccountFun, SettingsFun, LogFun
from Utils import ComUtils, HTMLUtils, logUtil


def getLayout(calledAccount = None):
    global cache
    if calledAccount is not None:
        calledAccount = ComUtils.makeValidURLReverse(calledAccount)
    globalVariables.accLast = calledAccount
    return [
        html.H2("Account Details"),
        html.Table([
            html.Tr([
                html.Th("Select account from Dropdown List"),
                html.Th("Log Amount"), html.Th("Control")
                ]),
            html.Tr([
                html.Td(dcc.Dropdown(
                    options=AccountFun.getAccountDropdown(), id='iAccount',value=calledAccount)),
                html.Td(dcc.Input(id='iAcc_log_amount',
                                  type='number', value='10', max='500')),
                html.Td([dcc.Dropdown(options=globalVariables.accountOptions, id='iAccount_Action'), html.Button(
                    'Perform Action', id="bAcc_Perform")])
                ])]),
        html.Div(id='account', children=AccountFun.getAccountHTML(calledAccount, 10) if calledAccount is not None else []),
        dcc.Interval(
            id='acc_interval', interval=globalVariables.WEBSITE_REFRESH_RATE/2, n_intervals=0),
        dcc.Interval(id='acc_drop_interval',
                     interval=15*1000, n_intervals=0)
        ]


def initCallbacks():
    @app.callback(Output('account', 'children'),
                  [Input('acc_interval', 'n_intervals'),Input('iAccount', 'value')],
                  # [Input('bAccount', 'n_clicks')],
                  [State('iAcc_log_amount', 'value')])
    def cb_Account(n, value, amount):
        if value is not None:
            globalVariables.accLast = value

        if globalVariables.accLast is not None:
            return AccountFun.getAccountHTML(globalVariables.accLast, int(amount)-1)
        else:
            pass

    @app.callback(Output('AccAction', 'children'),
                  [Input('bAcc_Perform', 'n_clicks')],
                  # [Input('bAccount', 'n_clicks')],
                  [State('iAccount', 'value'), State('iAccount_Action', 'value')])
    def cb_AccountAction(n, value, action):
        if value is not None:
            logUtil.log(1,"Will perform " + action + " for Account: " + value)
            logUtil.log(1,ComUtils.curlGet("bot/accounts/"+value+action))
        return []

    @app.callback(Output('iAccount', 'options'),
                  [Input('acc_drop_interval', 'n_intervals')])
    def cb_Drop_Account(n):
        return AccountFun.getAccountDropdown()
