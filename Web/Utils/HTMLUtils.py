from datetime import datetime, timedelta


def strHTML(pString):
    if not isinstance(pString, str):
        pString = str(pString)
    if "ä" in pString:
        pString.replace("ä", "&auml;")
    if "Ä" in pString:
        pString.replace("Ä", "&auml;")
    if "ö" in pString:
        pString.replace("ö", "&auml;")
    if "Ö" in pString:
        pString.replace("Ö", "&auml;")
    if "ü" in pString:
        pString.replace("ü", "&auml;")
    if "Ü" in pString:
        pString.replace("Ü", "&auml;")
    if "ß" in pString:
        pString.replace("ß", "&szlig;")
    if "&" in pString:
        pString.replace("&", "&amp;")
    if "<" in pString:
        pString.replace("<", "&lt;")
    if ">" in pString:
        pString.replace(">", "&gt;")
    return pString


def reformatLogTime(pTime, pFormat="%H:%M:%S"):
    # example: 2018-06-08T14:10:04.6063146+02:00

    if len(pTime) > 31:  # String with Timezone
        pTime = ''.join(pTime.rsplit(':', 1))
        pTime = pTime[:25] + pTime[26:]  # to fix 7 digit microseconds
        dt_object = datetime.strptime(pTime, "%Y-%m-%dT%H:%M:%S.%f%z")
    elif len(pTime) >= 30:  # String with Timezone 6 digits
        pTime = ''.join(pTime.rsplit(':', 1))
        dt_object = datetime.strptime(pTime, "%Y-%m-%dT%H:%M:%S.%f%z")
    elif len(pTime) >= 24:  # String without Timezone
        pTime = pTime[:24]  # to fix 7 digit microseconds
        dt_object = datetime.strptime(pTime, "%Y-%m-%dT%H:%M:%S.%f")
    else:  # String without Microseconds
        dt_object = datetime.strptime(pTime, "%Y-%m-%dT%H:%M:%S")
    return dt_object.strftime(pFormat)
