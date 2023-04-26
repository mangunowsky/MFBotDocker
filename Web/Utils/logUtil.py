# This Python file uses the following encoding: utf-8
from datetime import datetime, timedelta
from Functions import globalVariables
import colorama
colorama.init()

def log(pLevel, pMessage):
    if pLevel >= globalVariables.debugLevel:
        text = (str(datetime.now()) + " [" +
            globalVariables.debugLevels[pLevel] +
            "]: " + str(pMessage))
        open("log.txt","a", encoding='utf-8').write(text + "\n")
        string = globalVariables.debugColors[pLevel] + text + '\033[0m'
        print(string.encode('utf-8'))
