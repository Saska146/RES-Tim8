from datetime import datetime as d

def logData(data):
    timestamp = d.now()
    with open('loggerData.txt', 'a') as f:
        f.write(data + " -> logged at : " + timestamp.strftime('%d.%m.%Y. %H:%M:%S') + "\n")