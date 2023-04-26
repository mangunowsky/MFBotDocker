from Functions import globalVariables
from Utils import ComUtils, HTMLUtils, logUtil
from datetime import datetime, timedelta

import dash_core_components as dcc
import dash_html_components as html
import time


def updateBotLog():
    logUtil.log(2,"updating Bot Log")
    amount = globalVariables.CACHE_BOT_LOG["amount"]
    details = ComUtils.curlGet("Logs?count=" + str(amount))
    try:
        globalVariables.logs = details["response"]["logs"]
        successful = True
    except (KeyError):
        logUtil.log(4,"Key Error, remote response: " +str(details))
        successful = False
    if successful:
        globalVariables.CACHE_BOT_LOG["newData"] = True


def getLogsHTML(pAmount):
    logUtil.log(2,"Call for get Log, Amount: "+ str(pAmount))
    globalVariables.CACHE_BOT_LOG["lastRequest"] = datetime.now()
    if (pAmount >= globalVariables.CACHE_BOT_LOG["amount"]) or ((datetime.now() - globalVariables.CACHE_BOT_LOG["maxTime"]).total_seconds() > 30):
        globalVariables.CACHE_BOT_LOG["amount"] = pAmount
        globalVariables.CACHE_BOT_LOG["maxTime"] = datetime.now()
    if globalVariables.CACHE_BOT_LOG["newData"]:
        rCache = []
        logUtil.log(1,"Refresh log cache, amount: " + str(globalVariables.CACHE_BOT_LOG["amount"]))
        tableData = [html.Tr([
            html.Th("Time"),
            html.Th("Weight"),
            html.Th("Source"),
            html.Th("Entry")
            ])]
        amount = 0
        for l in reversed(globalVariables.logs):
            sTime = HTMLUtils.reformatLogTime(l["time"])
            tableData.append(html.Tr([
                html.Td(HTMLUtils.strHTML(sTime)),
                html.Td(HTMLUtils.strHTML(l["weight"])),
                html.Td(HTMLUtils.strHTML(l["source"])),
                html.Td(HTMLUtils.strHTML(l["entry"]))
                ]))
            amount += 1
            if amount > globalVariables.CACHE_BOT_LOG["amount"]:
                break
        rCache.append(html.Table(tableData))
        globalVariables.CACHE_BOT_LOG["data"] = rCache
        globalVariables.CACHE_BOT_LOG["newData"] = False
    return globalVariables.CACHE_BOT_LOG["data"]


def threadUpdateBotLog():
    while True:
        dif = (datetime.now() -
               globalVariables.CACHE_BOT_LOG["lastRequest"]).total_seconds()
        if dif < 40:
            logUtil.log(2,"Last Call for getBotLog " + str(dif) +
                  " s ago, going to update Bot Log")
            updateBotLog()
        time.sleep(globalVariables.REFRESH_RATE_ALL_DATA)
