import json
import wiotp.sdk.application
import requests


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
    CitizenTemperature = input("Enter the temperature of the citizen")
    CitizenDepartement = input("Enter the departement of the citizen")
    CitizenStatus = input ("Enter the status of the citizen")

    #JSONing Data
    myDeviceType = "DTC"
    myData={'temperature' : CitizenTemperature, 'departement' : CitizenDepartement, 'status' : CitizenStatus}

    #Publishing
    client.publishEvent(myDeviceType, myDeviceId, "CitizenStatus", "json", myData)
    print("Status of "+myDeviceId+" updated with values : "+CitizenTemperature+" for temperature and "+CitizenDepartement+" for departement")


# init
myConfig = wiotp.sdk.application.parseConfigFile("default-config.yaml")
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


# Connect




# client.subscribeToDeviceEvents(typeId="DTC",eventId="contact")


client.disconnect()