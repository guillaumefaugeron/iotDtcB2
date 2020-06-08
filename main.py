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

# Connect
client.connect()



print(client.registry.devices.get("kskdk"))
create_account = input("voulez-vous creer un compte (O/n) : ")

if create_account.lower() == "o" or "oui" :
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





# client.subscribeToDeviceEvents(typeId="DTC",eventId="contact")


client.disconnect()
