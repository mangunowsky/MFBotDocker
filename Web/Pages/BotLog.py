import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event, Input, State

from app import app
from Functions import globalVariables, AccountFun, SettingsFun, LogFun
from Utils import ComUtils, HTMLUtils, logUtil
cache = ""


def getLayout():
    logUtil.log(0,"Call for Botlog getLayout()")
    global cache
    if cache == "":
        cache = [
            html.H2("Global Bot Log"),
            dcc.Input(id='iBot_log_amount', type='number', value='10'),
            html.Div(id='logs_Container', children=[]),
            dcc.Interval(
                id='logs_interval', interval=globalVariables.WEBSITE_REFRESH_RATE/2, n_intervals=0)
            ]
    return cache


def initCallbacks():
    logUtil.log(0,"Creating Botlog Callbacks")
    @app.callback(Output('logs_Container', 'children'),
                  [Input('logs_interval', 'n_intervals')],
                  [State('iBot_log_amount', 'value')])
    def cb_Logs(n, value):
        logUtil.log(1,"CB logs fired")
        if value is not None:
            return LogFun.getLogsHTML(int(value))
