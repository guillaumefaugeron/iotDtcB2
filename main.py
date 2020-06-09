import json
import os
import json
from pathlib import Path

import wiotp.sdk.application
import requests
import base64
from login import login
from dotenv import load_dotenv

print(load_dotenv())
env_path = Path('.') / '.env'





api_key = os.getenv("api_key")
api_token = os.getenv("api_token")
orgid = os.getenv("orgid")
deviceid = ""
contacts = {}
user_credentials = {}
url_api = "https://" + orgid + ".internetofthings.ibmcloud.com/api/v0002/"
url_device_DTC = url_api + "device/types/DTC/devices"
headers = {'content-type': 'application/json'}


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
    print("3 : Je suis médecin")
    print("4 : Je suis admin")
    option = int(input())
    if option == 1:
        create = 0
        while create != 1:
            device_id = input("rentrer le nom du compte : ")
            auth_token = input("rentrer votre mot de passe : ")
            myobj = "{\"deviceId\": \""+ device_id + "\", \"authToken\": \"" + auth_token + "\"}"
            request = requests.post(url_device_DTC, data = myobj, headers=headers,  auth=(api_key, api_token))
            print(request)
            print(request.text)

            if request.status_code == 201:
                create = 1
                mydevice = device_id
                print("Compte créé")
            else:
                print(request.text)
    if option == 2:
        mydevice = input("rentrer le nom de votre compte")
        token = input("rentrer votre mdp")
        print(login(token,mydevice))
        role = "citoyen"
        user_credentials = {"role": role, "ID": mydevice}
    if option == 3:
        print("\nConnectez vous avec votre compte de médecin :")
        mydevice = input("rentrer le nom de votre compte")
        token = input("rentrer votre mdp")
        print(login(token,mydevice))
        role = "medecin"
        user_credentials = {"role": role, "ID": mydevice}
    if option == 4:
        print("\nConnectez vous avec votre compte d'admin :")
        mydevice = input("rentrer le nom de votre compte")
        token = input("rentrer votre mdp")
        print(login(token,mydevice))
        role = "admin"
        user_credentials = {"role": role, "ID": mydevice}


end = 0
while end != 1:
    print("Choisir une Option :")
    print("1 : Afficher la liste de mes contacts")
    print("2 : Déclencher un contact")
    print("3 : Publier son statut")
    print("4 : Publier sa temperature")
    print("5 : Quitter")
    if(user_credentials.get("role") == "medecin"):
        print("6 : Consulter la liste de suivi mes citoyens")
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
    if options == 6:
        myobj = """{"deviceId": "LeroyMerlin"}"""
        request = requests.get("https://zlmz36.internetofthings.ibmcloud.com/api/v0002/device/types/DTC/devices/LeroyMerlin/events", headers=headers, auth=(api_key, api_token))
        print(request.status_code)

        response_array = request.json()
        for dict in response_array:
            for key in dict:
                if(dict["eventId"] == "contact"):
                    content = dict["payload"]
                    print("Le citoyen à été en contact avec : %s" % (base64.b64decode(content).decode('utf-8')))

client.disconnect()