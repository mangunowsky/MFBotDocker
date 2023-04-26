import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event, Input, State
from datetime import datetime, timedelta

from app import app
from Functions import globalVariables, AccountFun, SettingsFun, LogFun
from Utils import ComUtils, HTMLUtils

cache = ""


def getLayout():
    global cache
    if cache == "":
        cache = [
            html.H2("Account Settings"),
            html.H3("Select desired account"),
            html.Table([
                html.Tr([html.Th("Select an account from the dropdown list"), html.Th(
                    "Choose the desired setting from the dropdown list")]),
                html.Tr([
                    html.Td(dcc.Dropdown(
                        options=AccountFun.getAccountDropdown(), id='iAccountSetting')),
                    html.Td(dcc.Dropdown(
                        options=AccountFun.getAccSettingsDropdown(), id='iSelectedSettingAcc'))
                    ])
                ]),
            dcc.RadioItems(
                options=[
                    {'label': 'Use sliders', 'value': '1'},
                    {'label': "Don't use sliders", 'value': '0'}
                    ], value=('0' if globalVariables.noSlider else '1'), id='slider_Selection'),
            html.Div(id='settingAcc', children=[]),
            html.H4("Changes to settings"),
            html.Button('Show/Refresh current changes',
                        id="bSettingsAcc_show", type="submit"),
            html.Button('Send changes to bot', id="bSettingsAcc_send", type="submit"),
            html.Button('Discard changes',
                        id="bSettingsAcc_delete", type="submit"),
            html.Div(id='Acc_Changes', children=[]),
            html.Div(id='Acc_Response', children=[]),
            html.Div(id='Acc_Delete', children=[])
            ]
    return cache


def initCallbacks():
    @app.callback(Output('settingAcc', 'children'),
                  [Input('iSelectedSettingAcc', 'value'), Input('iAccountSetting', 'value')],)
    def cb_View_settingAcc(c, pAccount):
        if pAccount is None:
            return html.H3("> Select an account")
        globalVariables.ACCOUNTS_o[pAccount].lastRequestS = datetime.now()
        if c is None:
            return html.H3("> Select a setting")
        return SettingsFun.getOneSetting(c, pAccount)

    @app.callback(Output('Acc_Response', 'children'),
                  [],
                  [State('iAccountSetting', 'value')],
                  [Event('bSettingsAcc_send', 'click')])
    def cb_send_settingsAcc(pAccount):
        if pAccount is None:
            return html.P("")
        if globalVariables.settingsChanges:
            r = SettingsFun.postSettings(pAccount)
            if r == "":
                return html.P(datetime.now().strftime("%H:%M:%S") + " settings posted")
            return html.P(datetime.now().strftime("%H:%M:%S") + " Error posting settings: " + HTMLUtils.strHTML(r))

    @app.callback(Output('Acc_Delete', 'children'),
                  [],
                  [State('iAccountSetting', 'value')],
                  [Event('bSettingsAcc_delete', 'click')])
    def cb_delete_settingsAcc(pAccount):
        if pAccount is None:
            return html.P("")
        if globalVariables.settingsChanges:
            globalVariables.settingsChanges = False
            globalVariables.account_Setting_Send[pAccount] = {}
            return html.P(datetime.now().strftime("%H:%M:%S") + " Changes discarded")

    @app.callback(Output('Acc_Changes', 'children'),
                  [],
                  [State('iAccountSetting', 'value')],
                  [Event('bSettingsAcc_show', 'click')])
    def cb_CurrentChangesAcc(pAccount):
        if pAccount is None:
            return html.P("")
        if globalVariables.settingsChanges:
            rCache = []
            rCache.append(
                html.P(datetime.now().strftime("%H:%M:%S")+" Changes:"))
            tableData = [html.Tr([html.Th("Name"), html.Th("Value")])]
            for b in globalVariables.account_Setting_Send[pAccount]:
                tableData.append(html.Tr([
                    html.Td(HTMLUtils.strHTML(
                        globalVariables.account_Setting_Send[pAccount][b]["key"])),
                    html.Td(HTMLUtils.strHTML(globalVariables.account_Setting_Send[pAccount][b]["value"]))]))
            rCache.append(html.Table(tableData))
            return rCache
