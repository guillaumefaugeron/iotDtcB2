import json
import wiotp.sdk.application
import requests
import base64



def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))



#Ici c le terter de arnaud
# Subrcribe to all DTC devices
def AdminSubscribeToAll():
    print("Subscribing to all DTC devices...")
    client.subscribeToDeviceEvents(typeId="DTC",eventId="CitizenStatus")

def MedicalUpdateStatus():
    #Inputs
    myDeviceId = input("Updating citizen status : Please type the ID of the Citizen : ")
    CitizenTemperature = input("Enter the temperature of the citizen : ")
    CitizenDepartement = input("Enter the departement of the citizen : ")
    submited = 0
    while submited != 1:
        CitizenStatus = input ("Enter the status of the citizen, 1 : sick , 2 : ok : ")
        if (int(CitizenStatus) == 1):
            CitizenStatus ="sick"
            submited = 1
        elif (int(CitizenStatus) == 2):
            CitizenStatus="ok"
            submited = 1
        else:
            print("Wrong number")

        #JSONing Data
        myDeviceType = "DTC"
        myData={'temperature' : CitizenTemperature, 'departement' : CitizenDepartement, 'status' : CitizenStatus}

        #Publishing
        client.publishEvent(myDeviceType, myDeviceId, "CitizenStatus", "json", myData)
        print("Status of "+myDeviceId+" updated with values : "+CitizenTemperature+" for temperature and "+CitizenDepartement+" for departement, the status is "+CitizenStatus)


# init
myConfig = wiotp.sdk.application.parseConfigFile("config.yaml")
client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)
client.deviceEventCallback = myEventCallback
client.commandCallback = myCommandCallback
client.connect()

updateStatus = input("Vous souhaitez mettre à jour le status d'un patient ? :")
if (updateStatus.lower() == "o") | (updateStatus.lower() == "oui"):
    MedicalUpdateStatus()
else:
   client.disconnect() 


create_account = input("Voulez-vous creer un compte (O/n) : ")
if (create_account.lower() == "o") | (create_account.lower() == "oui") :
    create = 0
    url_api = "https://vkrqyu.internetofthings.ibmcloud.com/api/v0002/"
    url_device_DTC = url_api + "device/types/DTC/devices"
    headers = {'content-type': 'application/json'}
    while create != 1:
        device_id = input("rentrer le nom du device : ")
        myobj = """{"deviceId": "%s"}""" %device_id
        request = requests.post(url_device_DTC, data = myobj, headers=headers,  auth=('a-vkrqyu-lfcnfan1no', '7ubBV0eEX_SAa&)?rN'))

        if request.status_code == 201:
            create = 1
            print(request.text)
        else:
            print(request.text)



def contact(name_device1, name_device2):
    client.subscribeToDeviceEvents(typeId="DTC", deviceId=name_device1, eventId="contact")
    device1 = {"typeId": "DTC", "deviceId": name_device1}
    event1 = client.lec.get(device1, "contact")
    print(event1.deviceId + (base64.b64decode(event1.payload).decode('utf-8')))
    client.subscribeToDeviceEvents(typeId="DTC", deviceId=name_device2, eventId="contact")
    device2 = {"typeId": "DTC", "deviceId": name_device2}
    event2 = client.lec.get(device2, "contact")
    print(event2.deviceId + (base64.b64decode(event2.payload).decode('utf-8')))

def publishStatus(device, status):
    myData={'status' : status}
    client.publishEvent("DTC", device, "contact", "json", myData)


# Connect



contact("test1", "test2")

publishStatus("test1", "ok")
publishStatus("test2", "malade")
# publishStatus("bgdu39", "malade")

# client.subscribeToDeviceEvents(typeId="DTC",eventId="contact")
while 1:
    a=0

client.disconnect()