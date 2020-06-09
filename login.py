import json
import os

import wiotp.sdk.application



def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))



def connect(token:str,deviceId:str):
    orgid = os.getenv("orgid")
    myConfig = {
    "identity": {
        "orgId": orgid,
        "typeId": "DTC",
        "deviceId": deviceId
    },
    "auth": {
        "token": token
    }
    }
    try :
        client = wiotp.sdk.device.DeviceClient(config=myConfig)
        client.connect()
        return deviceId
    except:
        return False





def login(token:str,deviceId:str):
    checkedToken = connect(token,deviceId)
    if checkedToken == deviceId:
        return deviceId
    else:
        while (checkedToken == False):
            newtoken = input("\n\n\nSAISIR LE BON MDP : ")
            checkedToken = connect(newtoken,deviceId)
        return deviceId



# print(login("kekel2enul","LeroyMerlin"))