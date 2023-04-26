from Functions import globalVariables
from Utils import logUtil
import pycurl
from io import BytesIO
import urllib
import json


def curlGet(pAppend=""):
    logUtil.log(0, "Call for curlGet("+pAppend+")")
    target = makeValidURL(globalVariables.ADRESS if pAppend == "" else globalVariables.ADRESS + pAppend)
    o = BytesIO()
    com = pycurl.Curl()
    com.setopt(pycurl.USERPWD, '{}:{}'.format(
        globalVariables.USERNAME, globalVariables.PASSWORD))
    com.setopt(com.URL, target)
    com.setopt(com.WRITEDATA, o)
    logUtil.log(2,"Performing GET adress: "+target)
    com.perform()
    com.close()
    # rString = o.getvalue().decode('iso-8859-1')
    rString = o.getvalue().decode('utf-8')
    return json.loads(rString)


def curlPost(pObject, pAppend=""):
    logUtil.log(0, "Call for curlPost("+pAppend+"), with Data: " +str(pObject))
    target = makeValidURL(globalVariables.ADRESS if pAppend == "" else globalVariables.ADRESS  + pAppend)
    sendData = json.dumps(pObject)
    logUtil.log(2,"Performing Post to "+target+" , Data:" + sendData)
    o = BytesIO()
    com = pycurl.Curl()
    com.setopt(pycurl.USERPWD, '{}:{}'.format(
        globalVariables.USERNAME, globalVariables.PASSWORD))
    com.setopt(com.URL, target)
    com.setopt(com.WRITEDATA, o)
    com.setopt(pycurl.POST, 1)
    com.setopt(pycurl.POSTFIELDS, sendData)
    com.perform()
    com.close()
    # rString = o.getvalue().decode('iso-8859-1')
    rString = o.getvalue().decode('utf-8')
    return json.loads(rString)

def makeValidURL(pUrl):
    logUtil.log(0, "Call for makeValidURL("+pUrl+")")
    return urllib.parse.quote_plus(pUrl.replace(" ", "%20"), safe="-._~:/?#[]@!$&()*+,='%")

def makeValidURLReverse(pUrl):
    logUtil.log(0, "Call for makeValidURLReverse("+pUrl+")")
    return urllib.parse.unquote_plus(pUrl.replace("%20", " "))
