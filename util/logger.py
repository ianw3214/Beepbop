import datetime

def log(module, message):
    currTime = datetime.datetime.now()
    timeInfo = currTime.strftime("[%m/%d/%Y, %H:%M:%S] ")
    print(timeInfo + module + ": " + message)