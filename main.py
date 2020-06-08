import json
import wiotp.sdk.application
import requests


def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))

# init
myConfig = wiotp.sdk.application.parseConfigFile("config.yaml")
client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)
client.deviceEventCallback = myEventCallback
client.commandCallback = myCommandCallback


create_account = input("voulez-vous creer un compte (O/n) : ")

if (create_account.lower() == "o") | (create_account.lower() == "oui") :
    create = 0
    while create != 1:
        url_api = "https://vkrqyu.internetofthings.ibmcloud.com/api/v0002/"
        url_device_DTC = url_api + "device/types/DTC/devices"
        headers = {'content-type': 'application/json'}
        device_id = input("rentrer le nom du device : ")

        myobj = """{"deviceId": "%s"}""" %device_id
        request = requests.post(url_device_DTC, data = myobj, headers=headers,  auth=('a-vkrqyu-lfcnfan1no', '7ubBV0eEX_SAa&)?rN'))

        if request.status_code == 201:
            create = 1
            print(request.text)
        else:
            print(request.text)



def contact(device1, device2):
    client.subscribeToDeviceEvents(typeId="DTC", deviceId=device1, eventId="contact")
    client.subscribeToDeviceEvents(typeId="DTC", deviceId=device2, eventId="contact")

def publishStatus(device, status):
    myData={'status' : status}
    client.publishEvent("DTC", device, "contact", "json", myData)


# Connect
client.connect()


contact("test1", "test2")

publishStatus("test1", "ok")
publishStatus("test1", "malade")
publishStatus("bgdu39", "malade")

# client.subscribeToDeviceEvents(typeId="DTC",eventId="contact")
while 1:
    a=0

client.disconnect()
