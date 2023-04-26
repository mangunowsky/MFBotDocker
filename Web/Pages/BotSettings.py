import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
from datetime import datetime, timedelta

from app import app
from Functions import globalVariables, AccountFun, SettingsFun, LogFun
from Utils import HTMLUtils, ComUtils

cache = ""


def getLayout():
    global cache
    if cache == "":
        cache = [
            html.H2("Account Settings"),
            dcc.Dropdown(options=getSettingsDropdown(), id='iSelectedSetting'),
            dcc.RadioItems(
                options=[
                    {'label': 'Use sliders', 'value': '1'},
                    {'label': "Don't use sliders", 'value': '0'}
                    ], value=('0' if globalVariables.noSlider else '1'), id='slider_Selection'),
            html.Div(id='setting', children=[]),
            html.H3("Changes to settings"),
            html.Button('Show/Refresh current changes', id="bSettings_show", type="submit"),
            html.Button('Send changes to bot', id="bSettings_send", type="submit"),
            html.Button('Discard changes to settings', id="bSettings_delete", type="submit"),
            html.Div(id='global_Changes', children=[]),
            html.Div(id='global_Response', children=[]),
            html.Div(id='global_Delete', children=[]),
            dcc.Interval(id='settings_interval',
                         interval=globalVariables.WEBSITE_REFRESH_RATE, n_intervals=0),
            html.Div(id='Settings_Empty')
            ]
    return cache


def getSettingsDropdown():
    return[{'label': a, 'value': a} for a in globalVariables.SETTING_LIST]


def initCallbacks():
    @app.callback(Output('setting', 'children'),
                  [Input('iSelectedSetting', 'value')])
    def cb_View_setting(c):
        if c is not None:
            return SettingsFun.getOneSetting(c, "")
        return html.H3("> Select a setting")

    @app.callback(Output('global_Response', 'children'),
                  [],
                  [],
                  [Event('bSettings_send', 'click')])
    def cb_send_settings():
        if globalVariables.settingsChanges:
            r = SettingsFun.postSettings("")
            if r == "":
                return html.P(datetime.now().strftime("%H:%M:%S") + " Settings Posted")
            return html.P(datetime.now().strftime("%H:%M:%S") + " Error Posting Settings: " + HTMLUtils.strHTML(r))

    @app.callback(Output('global_Delete', 'children'),
                  [],
                  [],
                  [Event('bSettings_delete', 'click')])
    def cb_delete_settings():
        if globalVariables.settingsChanges:
            globalVariables.settingsChanges = False
            globalVariables.settings_send = {}
            return html.P(datetime.now().strftime("%H:%M:%S") + " Changes discarded")

    @app.callback(Output('global_Changes', 'children'),
                  [],
                  [],
                  [Event('bSettings_show', 'click')])
    def cb_CurrentChanges():
        if globalVariables.settingsChanges:
            rCache = []
            rCache.append(
                html.P(datetime.now().strftime("%H:%M:%S")+" Changes:"))
            tableData = [html.Tr([html.Th("Name"), html.Th("Value")])]
            for a in globalVariables.settings_send:
                tableData.append(html.Tr([
                    html.Td(HTMLUtils.strHTML(
                        globalVariables.settings_send[a]["key"])),
                    html.Td(HTMLUtils.strHTML(globalVariables.settings_send[a]["value"]))]))
            rCache.append(html.Table(tableData))
            return rCache

    @app.callback(Output('Settings_Empty', 'children'),
                  [Input('settings_interval', 'n_intervals')])
    def cb_SettingsInt(c):
        globalVariables.GLOBAL_SETTINGS_lastRequest = datetime.now()
