import json
import wiotp.sdk.application
import requests
import base64

contacts = {}

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def myEventCallback(event):
    contacts[event.deviceId].update(event.data)
    str = "%s event '%s' received from device %s : %s"
    print(str % (event.format, event.eventId, event.deviceId, json.dumps(event.data)))

def contact(name_device):
    client.subscribeToDeviceEvents(typeId="DTC", deviceId=name_device, eventId="CitizenStatus")
    device = {"typeId": "DTC", "deviceId": name_device}
    event = client.lec.get(device, "CitizenStatus")
    contacts[name_device] = json.loads(base64.b64decode(event.payload).decode('utf-8'))

def publishStatus(device, status):
    myData={'status' : status}
    client.publishEvent("DTC", device, "CitizenStatus", "json", myData)

def publishTemp(device, temp):
    myData={'temp' : temp}
    client.publishEvent("DTC", device, "CitizenStatus", "json", myData)


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

mydevice = ""

while not mydevice :
    print("Choisir une Option :")
    print("1 : Creer un compte")
    print("2 : Se connecter")
    option = int(input())
    if option == 1:
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
                mydevice = device_id
                print("Compte créé")
            else:
                print(request.text)
    if option == 2:
        mydevice = input("rentrer le nom de votre device")


end = 0
while end != 1:
    print("Choisir une Option :")
    print("1 : Afficher la liste de mes contacts")
    print("2 : Déclencher un contact")
    print("3 : Publier son statut")
    print("4 : Publier sa temperature")
    print("5 : Quitter")
    options = int(input())
    if options == 1:
        print(contacts)
    if options == 2:
        device_name = input("Rentrer le nom du device que vous avez rencontré (c'est une simulation normalement c'est automatique) : ")
        contact(device_name)
    if options == 3:
        status = input("Rentrer votre status : ")
        # faire un check pour que se soit que (suspect, ok ou malade)
        publishStatus(mydevice, status)
    if options == 4:
        temp = input("Rentrer votre temperature : ")
        publishTemp(mydevice, temp)
    if options == 5:
        end = 1
    

client.disconnect()