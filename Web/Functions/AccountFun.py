from Functions import globalVariables
from Utils import ComUtils, HTMLUtils, logUtil

from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import time


class Account:
    def __init__(self, pName, pLogs):
        self.name = pName
        self.settings = {}
        self.log = pLogs
        self.amount = 10
        # in the past to prevent initial updates
        self.lastRequestS = datetime.now() - timedelta(minutes=15)
        # in the past to prevent initial updates
        self.lastRequestL = datetime.now() - timedelta(minutes=15)
        self.lastUpdateL = datetime.now() - timedelta(minutes=15)
        self.logData = []
        self.newDataL = False
        self.maxTime = datetime.now()


def getAccountDropdown():
    return[{'label': a, 'value': a} for a in globalVariables.account_names]


def getAccSettingsDropdown():
    return[{'label': a, 'value': a} for a in globalVariables.ACC_SETTING_LIST]


def updateAccs(pResetTime=True):
    logUtil.log(1,"updating Accs")
    details = ComUtils.curlGet("?head=1")
    try:
        globalVariables.accounts = details["response"]["bot"]["accounts"]
        successful = True
    except (KeyError):
        logUtil.log(4,"Key Error, remote Response:" + str(details))
        successful = False
    if successful:
        globalVariables.account_names = []
        for o in globalVariables.accounts:
            for key in o.keys():
                globalVariables.account_names.append(key)
                if not key in globalVariables.ACCOUNTS_o.keys():
                    globalVariables.ACCOUNTS_o[key] = Account(key, [])
                    if pResetTime:
                        globalVariables.ACCOUNTS_o[key].lastRequestL = datetime.now(
                            )
                        globalVariables.ACCOUNTS_o[key].lastRequestS = datetime.now(
                            )
        globalVariables.CACHE_ACCS["newData"] = True


def updateAccLog(pAccount):
    logUtil.log(2,"updating Bot Log")
    amount = globalVariables.ACCOUNTS_o[pAccount].amount
    details = ComUtils.curlGet(
        "bot/Accounts/"+pAccount+"/Logs?count=" + str(amount))
    try:
        globalVariables.ACCOUNTS_o[pAccount].log = details["response"]["logs"]
        successful = True
    except (KeyError):
        logUtil.log(4,"Key Error, remote Response:" + str(details))
        successful = False
    if successful:
        globalVariables.ACCOUNTS_o[pAccount].newDataL = True
        globalVariables.ACCOUNTS_o[pAccount].lastUpdateL = datetime.now()


def getAccounts(pSelection):
    globalVariables.CACHE_ACCS["lastRequest"] = datetime.now()
    if globalVariables.CACHE_ACCS["newData"]:
        CurrentHeader = []
        CurrentTable = []
        CurrentHeader.append(html.Th("Name"))
        for a in pSelection:
            CurrentHeader.append(html.Th(HTMLUtils.strHTML(
                globalVariables.columHeaders[a]["label"])))
        CurrentTable.append(html.Tr(CurrentHeader))
        for a in globalVariables.accounts:
            for currentAccName in a.keys():
                currentAcc = a[currentAccName]
                CurrentBody = []
                CurrentBody.append(html.Td(dcc.Link(HTMLUtils.strHTML(currentAccName), href='/Account/' + ComUtils.makeValidURL(currentAccName))))
                for b in pSelection:
                    if b in currentAcc.keys():
                        if globalVariables.columHeaders[b]["type"] == "":
                            tdText = HTMLUtils.strHTML(currentAcc[b])
                        elif globalVariables.columHeaders[b]["type"] == "beer":
                            tdText = HTMLUtils.strHTML(
                                str(currentAcc[b]) + "/11")
                        elif globalVariables.columHeaders[b]["type"] == "time":
                            tdText = HTMLUtils.strHTML(
                                HTMLUtils.reformatLogTime(currentAcc[b], "%d.%m %H:%M:%S"))
                        elif globalVariables.columHeaders[b]["type"] == "percent":
                            tdText = HTMLUtils.strHTML(
                                "{0:.2f}%".format(float(currentAcc[b])))
                    else:
                        tdText = ""
                    CurrentBody.append(html.Td(tdText))
                CurrentTable.append(html.Tr(CurrentBody))
        globalVariables.CACHE_ACCS["data"] = html.Table(CurrentTable)
        globalVariables.CACHE_ACCS["newData"] = False
    return globalVariables.CACHE_ACCS["data"]


def getAccountHTML(pAccount, pLogAmount):
    if not pAccount == "":
        n = datetime.now()
        secondsDiff = (n-globalVariables.ACCOUNTS_o[pAccount].lastUpdateL).total_seconds()
        if (pLogAmount >= globalVariables.ACCOUNTS_o[pAccount].amount) or ((n - globalVariables.ACCOUNTS_o[pAccount].maxTime).total_seconds() > 30):
            globalVariables.ACCOUNTS_o[pAccount].amount = pLogAmount
            globalVariables.ACCOUNTS_o[pAccount].maxTime = n
        globalVariables.ACCOUNTS_o[pAccount].lastRequestL = n
        if secondsDiff > 40:
            logUtil.log(3,"Last r was "+str(secondsDiff)+" s ago")
            rCache=[html.H2(
                "Last data refresh was "+HTMLUtils.strHTML(secondsDiff)+" s ago. Fetching data.."
                )]
            rCache.extend(globalVariables.ACCOUNTS_o[pAccount].logData)
            return rCache
        if globalVariables.ACCOUNTS_o[pAccount].newDataL:
            rCache = []
            rCache.append(html.H3("Log for Account: " + pAccount))
            LogData = [html.Tr([
                html.Th("Time"),
                html.Th("Weight"),
                html.Th("Source"),
                html.Th("Entry")
                ])]
            amount = 0
            for l in reversed(globalVariables.ACCOUNTS_o[pAccount].log):
                sTime = HTMLUtils.reformatLogTime(l["time"])
                LogData.append(html.Tr([
                    html.Td(HTMLUtils.strHTML(sTime)),
                    html.Td(HTMLUtils.strHTML(l["weight"])),
                    html.Td(HTMLUtils.strHTML(l["source"])),
                    html.Td(HTMLUtils.strHTML(l["entry"])),
                    ]))
                amount += 1
                if amount > pLogAmount:
                    break
            rCache.append(html.Table(LogData))
            globalVariables.ACCOUNTS_o[pAccount].logData = rCache
            globalVariables.ACCOUNTS_o[pAccount].newDataL = False
        return globalVariables.ACCOUNTS_o[pAccount].logData
    return html.P("Please select an Account")


def threadUpdateAccs():
    while True:
        dif = (datetime.now() -
               globalVariables.CACHE_ACCS["lastRequest"]).total_seconds()
        if dif < 40:
            logUtil.log(3,"Last Call for getAccounts " + str(dif) +
                  " s ago, going to update Acc Overview")
            updateAccs()
        time.sleep(globalVariables.REFRESH_RATE_ALL_DATA)


def threadUpdateAccountLog():
    while True:
        # n = datetime.now() -timedelta(seconds=40)
        # for a in ACCOUNTS_o:
        #     if ACCOUNTS_o[a].lastRequestL > n: updateAccLog(a)
        n = datetime.now()
        for a in globalVariables.ACCOUNTS_o:
            dif = (
                n-globalVariables.ACCOUNTS_o[a].lastRequestL).total_seconds()
            if dif < 40:
                logUtil.log(2,"Last Call for getAccLog (Account: " + a + ") " +
                      str(dif) + " s ago, going to update Bot Log")
                updateAccLog(a)
        time.sleep(globalVariables.REFRESH_RATE_ALL_DATA)
