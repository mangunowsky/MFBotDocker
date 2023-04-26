from Functions import globalVariables
from Utils import ComUtils, HTMLUtils, logUtil
from app import app
from dash.dependencies import Output, Event, Input, State

import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
import time


class Setting:
    def __init__(self, pKey, pValue, pType, pAdvanced, params, pDescription, pGlobal=True, pAccount=""):
        self.key = pKey
        self.value = pValue
        self.type = pType
        self.description = pDescription
        self.advancedSetting = pAdvanced
        self.validationParameter = params
        self.isGlobal = pGlobal
        self.Account = pAccount
        self.fixedKey = (
            "global_" + pKey if pGlobal else "acc_" + pKey).replace(".", "_")
        # self.fixedKey = pKey.replace(".","_")
        if not pGlobal:
            if self.fixedKey not in globalVariables.callbackList:
                app.callback(
                    Output("div_"+self.fixedKey, 'children'),
                    [Input("iSetting_"+self.fixedKey, 'value')], [State('iAccountSetting', 'value'), State('iSelectedSettingAcc', 'value')])(self.generateAccSettingCb())
                globalVariables.callbackList.append(self.fixedKey)
            logUtil.log(0,"Fixed Key for Setting Object: " +self.fixedKey)
            if not self.key in globalVariables.ACC_SETTING_LIST:
                globalVariables.ACC_SETTING_LIST.append(self.key)
            if not pAccount in globalVariables.account_Setting_Send:
                globalVariables.account_Setting_Send[pAccount] = {}
        else:
            app.callback(
                Output("div_"+self.fixedKey, 'children'),
                [Input("iSetting_"+self.fixedKey, 'value')])(self.generateSettingCb())
            if not self.key in globalVariables.SETTING_LIST:
                globalVariables.SETTING_LIST.append(self.key)

    def appendToSetting_send(self, newVal):
        globalVariables.settingsChanges = True
        if self.isGlobal:
            if self.key in globalVariables.settings_send.keys():
                globalVariables.settings_send[self.key]["value"] = newVal
            else:
                globalVariables.settings_send[self.key] = {
                    "key": self.key, "value": newVal}
        else:
            cAccount = self.Account
            if self.key in globalVariables.account_Setting_Send[cAccount].keys():
                globalVariables.account_Setting_Send[cAccount][self.key]["value"] = newVal
            else:
                globalVariables.account_Setting_Send[cAccount][self.key] = {
                    "key": self.key, "value": newVal}
                logUtil.log(2,"Current setting send for "+cAccount + ": " +
                    str(globalVariables.account_Setting_Send[cAccount]))

    def generateSettingCb(self):
        def cb_General_Setting(a):
            if self.type == "Double" or self.type == "Int32":
                if "min" in self.validationParameter.keys():
                    if float(a) < float(self.validationParameter["min"]["value"]):
                        return html.P("Accepted Minimum is" + HTMLUtils.strHTML(self.validationParameter["min"]["value"]))
                if "max" in self.validationParameter.keys():
                    if float(a) > float(self.validationParameter["max"]["value"]):
                        return html.P("Accepted Maximum is" + HTMLUtils.strHTML(self.validationParameter["max"]["value"]))
            if self.value == str(a):
                logUtil.log(3,"Value didn`t Change for "+self.key +
                      " (Account: "+self.Account+"), maybe Page Load")
                return html.P("")
            logUtil.log(2,"Changed " + self.key +
                  "(Account: "+self.Account+") to " + str(a))
            self.appendToSetting_send(a)
            return html.P("Prepared Change to " + HTMLUtils.strHTML(a))
        return cb_General_Setting

    def generateAccSettingCb(self):
        def cb_Acc_Setting(a, val, key):
            if globalVariables.ACCOUNTS_o[val].settings[key].type == "Double" or globalVariables.ACCOUNTS_o[val].settings[key].type == "Int32":
                if "min" in globalVariables.ACCOUNTS_o[val].settings[key].validationParameter.keys():
                    if float(a) < float(globalVariables.ACCOUNTS_o[val].settings[key].validationParameter["min"]["value"]):
                        return html.P("Accepted Minimum is" + HTMLUtils.strHTML(globalVariables.ACCOUNTS_o[val].settings[key].validationParameter["min"]["value"]))
                if "max" in globalVariables.ACCOUNTS_o[val].settings[key].validationParameter.keys():
                    if float(a) > float(globalVariables.ACCOUNTS_o[val].settings[key].validationParameter["max"]["value"]):
                        return html.P("Accepted Maximum is" + HTMLUtils.strHTML(globalVariables.ACCOUNTS_o[val].settings[key].validationParameter["max"]["value"]))
            if globalVariables.ACCOUNTS_o[val].settings[key].value == str(a):
                logUtil.log(3,"Value didn`t Change for "+globalVariables.ACCOUNTS_o[val].settings[key].key +
                      " (Account: "+globalVariables.ACCOUNTS_o[val].settings[key].Account+"), maybe Page Load")
                return html.P("")
            logUtil.log(2,"Changed " + globalVariables.ACCOUNTS_o[val].settings[key].key +
                  "(Account: "+globalVariables.ACCOUNTS_o[val].settings[key].Account+") to " + str(a))
            globalVariables.ACCOUNTS_o[val].settings[key].appendToSetting_send(
                a)
            return html.P("Prepared Change to " + HTMLUtils.strHTML(a))
        return cb_Acc_Setting

    def getHtml(self):
        iElement = {}
        if "valueList" in self.validationParameter.keys():
            iElement = [
                dcc.Dropdown(options=[{'label': a, 'value': a} for a in self.validationParameter["valueList"]
                                      ["value"]], id="iSetting_"+self.fixedKey, value=self.value),
                html.Div(id="div_"+self.fixedKey, children=[]  # , style={'display':'none'}
                         )]
        elif ("min" in self.validationParameter.keys()) and (not self.type == "TimeSpan"):

            if "precision" in self.validationParameter.keys():
                prec = float(self.validationParameter["precision"]["value"])
                slide_step = 1/(10 ** prec)
            else:
                slide_step = 0.1 if (self.type == "Double") else 1
            slide_min = float(self.validationParameter["min"]["value"]) if (
                self.type == "Double") else int(self.validationParameter["min"]["value"])
            slide_max = float(self.validationParameter["max"]["value"]) if (
                self.type == "Double") else int(self.validationParameter["max"]["value"])
            slide_dist = slide_max - slide_min
            slide_val = float(self.value) if (
                self.type == "Double") else int(self.value)
            if slide_dist > 100.9 or globalVariables.noSlider:
                iElement = [
                    dcc.Input(type='number', min=slide_min, max=slide_max,
                              step=slide_step, id="iSetting_"+self.fixedKey, value=slide_val),
                    html.Div(id="div_"+self.fixedKey, children=[]  # , style={'display':'none'}
                             )]
            else:
                iElement = [
                    dcc.Slider(min=slide_min, max=slide_max, step=slide_step,
                               id="iSetting_"+self.fixedKey, value=slide_val),
                    html.Div(id="div_"+self.fixedKey, children=[]  # , style={'display':'none'}
                             )]
        elif self.type == "String" or self.type == "MailAddress" or self.type == "TimeSpan":
            if self.type == "String":
                cType = 'text'
            elif self.type == "MailAddress":
                cType = 'MailAddress'
            elif self.type == "TimeSpan":
                cType = 'time'
            iElement = [
                dcc.Input(type=cType, id="iSetting_" +
                          self.fixedKey, value=self.value),
                html.Div(id="div_"+self.fixedKey, children=[]  # , style={'display':'none'}
                         )]
        else:
            iElement = HTMLUtils.strHTML(self.validationParameter)
        tHeader = [
            html.Th("Name"),
            html.Th("Value"),
            html.Th("type"),
            html.Th("Advanced"),
            html.Th("Change")
            ]
        if not self.description == "":
            tHeader.append(html.Th("Description"))
        tSetting = [
            html.Td(HTMLUtils.strHTML(self.key)),
            html.Td(HTMLUtils.strHTML(self.value)),
            html.Td(HTMLUtils.strHTML(self.type)),
            html.Td(HTMLUtils.strHTML(self.advancedSetting)),
            html.Td(iElement)
            ]
        if not self.description == "":
            tHeader.append(html.Td(HTMLUtils.strHTML(self.description)))
        return [html.Tr(tHeader), html.Tr(tSetting)]
    # def __repr__(self):
    #     return json.dumps(self.__dict__)


def parseSettings(pSettingsArray, pAccount="", pValues=True):
    for s in pSettingsArray:
        name = s["key"]
        if pAccount == "":
            if name in globalVariables.settings.keys():
                globalVariables.settings[name].value = s["value"]
                continue
        else:
            if name in globalVariables.ACCOUNTS_o[pAccount].settings.keys():
                globalVariables.ACCOUNTS_o[pAccount].settings[name].value = s["value"]
                continue
        params = {}
        desc = s["description"] if "description" in s.keys() else ""
        if "validationParameter" in s.keys():
            for p in s["validationParameter"]:
                for k in p.keys():
                    params[k] = {"name": k, "value": p[k]}
            valParse = s["value"] if pValues else ""
            if pAccount == "":
                globalVariables.settings[name] = Setting(
                    s["key"], valParse, s["validationName"], s["isAdvancedSetting"], params, desc)
            else:
                globalVariables.ACCOUNTS_o[pAccount].settings[name] = Setting(
                    s["key"], valParse, s["validationName"], s["isAdvancedSetting"], params, desc, False, pAccount)
        else:
            logUtil.log(4,"Setting " + name+" has no Validation Parameters")


def postSettings(pAcc=""):
    error = "Nothing changed Yet"
    if pAcc == "":
        if len(globalVariables.settings_send) > 0:
            aSendSettings = []
            for s in globalVariables.settings_send:
                aSendSettings.append(globalVariables.settings_send[s])
            o = {"settings": aSendSettings}
            r = ComUtils.curlPost(o, "Settings")
            try:
                aSettings = r["response"]["settings"]
                successful = True
            except (KeyError):
                successful = False
                error = r
            if successful:
                parseSettings(aSettings)
                globalVariables.settings_send = {}
                error = ""
    else:
        if len(globalVariables.account_Setting_Send[pAcc]) > 0:
            aSendSettings = []
            for s in globalVariables.account_Setting_Send[pAcc]:
                aSendSettings.append(
                    globalVariables.account_Setting_Send[pAcc][s])
            o = {"settings": aSendSettings}
            r = ComUtils.curlPost(
                o, "bot/Accounts/" + pAcc+"/Settings")
            try:
                aSettings = r["response"]["settings"]
                successful = True
            except (KeyError):
                successful = False
                error = r
            if successful:
                if error == "Nothing changed Yet":
                    error = ""
                parseSettings(aSettings, pAcc)
                globalVariables.account_Setting_Send[pAcc] = {}
                error = ""
    amount = len(globalVariables.settings_send)
    for a in globalVariables.account_Setting_Send:
        amount += len(globalVariables.account_Setting_Send[a])
    if amount == 0:
        globalVariables.settingsChanges = False
    return error


def updateSettings(pAccount=""):
    # print("updating Bot Log")
    if pAccount == "":
        details = ComUtils.curlGet("Settings")
    else:
        details = ComUtils.curlGet(
            "/bot/Accounts/"+pAccount+"/Settings")
    successful = False
    try:
        aSettings = details["response"]["settings"]
        successful = True
    except (KeyError):
        print("Key Error:")
        print(details)
        successful = False
    if successful:
        parseSettings(aSettings, pAccount)


def getOneSetting(pKey, pAcc=""):
    if not pKey == "":
        rCache = []
        rCache.append(html.H3("Setting "+pKey+":"))
        a = globalVariables.settings[pKey] if(
            pAcc == "") else globalVariables.ACCOUNTS_o[pAcc].settings[pKey]
        rCache.append(html.Table(a.getHtml()))
        return rCache
    return html.P("No Key selected, you need to click again after selection")


def getSettingsMeta(pAccount=""):
    if pAccount == "":
        details = ComUtils.curlGet("Settings!GetMetaInfo")
    else:
        details = ComUtils.curlGet(
            "bot/Accounts/"+pAccount+"/Settings!GetMetaInfo")
    try:
        aSettings = details["response"]
        successful = (details['responseMeta']["responseType"] == "Array")
    except (KeyError):
        logUtil.log(4,"Key Error, Remote response: " + str(details))
        successful = False
        return False
    if successful:
        parseSettings(aSettings, pAccount, False)
    else:
        logUtil.log(4,"Unknown MetaData Error, Remote response: " + str(details))


def threadUpdateSettings():
    while True:
        n = datetime.now()
        # n = datetime.now() -timedelta(seconds=40)
        for a in globalVariables.ACCOUNTS_o:
            #     if ACCOUNTS_o[a].lastRequestS > n: updateSettings(a)
            # if GLOBAL_SETTINGS_lastRequest > n: updateSettings():
            dif = (
                n-globalVariables.ACCOUNTS_o[a].lastRequestS).total_seconds()
            if dif < 40:
                logUtil.log(2,"Last Call for getAccSettings (Account: " + a + ") " +
                      str(dif) + " s ago, going to update Account Settings")
                updateSettings(a)
        dif = (n-globalVariables.GLOBAL_SETTINGS_lastRequest).total_seconds()
        if dif < 40:
            logUtil.log(2,"Last Call for getGlobalSettings " + str(dif) +
                  " s ago, going to update Global Settings")
            updateSettings()
        time.sleep(globalVariables.REFRESH_RATE_ALL_DATA)
