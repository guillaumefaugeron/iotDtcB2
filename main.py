import json
import os
import json
from pathlib import Path

import wiotp.sdk.application
import requests
import base64
from login import login
from dotenv import load_dotenv
import time

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
url_delete_device_DTC = url_api + "device/types/DTC/devices/"
headers = {'content-type': 'application/json'}


def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def suspect(status_contact, name_device):
    device = {"typeId": "DTC", "deviceId": name_device}
    event = client.lec.get(device, "CitizenStatus")
    my_status = json.loads(base64.b64decode(event.payload).decode('utf-8'))["status"]
    if status_contact == "malade"and my_status != "malade":
        publishStatus(name_device, "suspect")

def deleteDevice(name_device):
    requests.delete(url_delete_device_DTC + name_device, auth=(api_key, api_token))

def myEventCallback(event):
    contacts[event.deviceId].update(event.data)
    suspect(contacts[event.deviceId]['status'], mydevice)
    str = "%s event '%s' received from device %s : %s"
    print(str % (event.format, event.eventId, event.deviceId, json.dumps(event.data)))

def contact(name_device):
    client.subscribeToDeviceEvents(typeId="DTC", deviceId=name_device, eventId="CitizenStatus")
    device = {"typeId": "DTC", "deviceId": name_device}
    event = client.lec.get(device, "CitizenStatus")
    contacts[name_device] = json.loads(base64.b64decode(event.payload).decode('utf-8'))
    suspect(contacts[name_device]['status'], mydevice)

def publishStatus(device, status):
    myData={'status' : status}
    client.publishEvent("DTC", device, "CitizenStatus", "json", myData)

def publishTemp(device, temp):
    myData={'temp' : temp}
    client.publishEvent("DTC", device, "Temperature", "json", myData)


#Ici c le terter de arnaud
# Subrcribe to all DTC devices
def AdminSubscribeToAll():
    print("Subscribing to all DTC devices...")
    client.subscribeToDeviceEvents(typeId="DTC",eventId="CitizenStatus")

def MedicalUpdateStatus():
    #Inputs
    myDeviceId = input("Updating citizen status : Please type the ID of the Citizen : ")
    CitizenDepartement = input("Enter the departement of the citizen : ")
    submited = 0
    while submited != 1:
        CitizenStatus = input ("Enter le status du citoyen , 1 : malade , 2 : ok , 3 : suspect ")
        if (int(CitizenStatus) == 1):
            CitizenStatus ="malade"
            submited = 1
        elif (int(CitizenStatus) == 2):
            CitizenStatus="ok"
            submited = 1
        elif (int(CitizenStatus) == 3):
            CitizenStatus="suspect"
            submited = 1
        else:
            print("Wrong number")

        #JSONing Data
        myDeviceType = "DTC"
        myData={'departement' : CitizenDepartement, 'status' : CitizenStatus}

        #Publishing
        client.publishEvent(myDeviceType, myDeviceId, "CitizenStatus", "json", myData)
        print("Status of "+myDeviceId+" updated with values : " + CitizenDepartement+" for departement, the status is "+CitizenStatus)


# init
myConfig = wiotp.sdk.application.parseConfigFile("config.yaml")
client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)
client.deviceEventCallback = myEventCallback
client.commandCallback = myCommandCallback
client.connect()

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
                time.sleep(1)
            else:
                print(request.text)
    if option == 2:
        mydevice = input("rentrer le nom de votre compte : ")
        token = input("rentrer votre mdp : ")
        print(login(token,mydevice))
        role = "citoyen"
        user_credentials = {"role": role, "ID": mydevice}
        time.sleep(1)

    if option == 3:
        print("\nConnectez vous avec votre compte de médecin : ")
        mydevice = input("rentrer le nom de votre compte : ")
        token = input("rentrer votre mdp : ")
        print(login(token,mydevice))
        role = "medecin"
        user_credentials = {"role": role, "ID": mydevice}
        time.sleep(1)
    if option == 4:
        print("\nConnectez vous avec votre compte d'admin :")
        mydevice = input("rentrer le nom de votre compte : ")
        token = input("rentrer votre mdp : ")
        print(login(token,mydevice))
        role = "admin"
        user_credentials = {"role": role, "ID": mydevice}
        time.sleep(1)


end = 0
while end != 1:
    time.sleep(1)
    print("Choisir une Option :")
    print("1 : Afficher la liste de mes contacts")
    print("2 : Déclencher un contact")
    print("3 : Publier son statut")
    print("4 : Publier sa temperature")
    print("5 : Quitter")
    if(user_credentials.get("role") == "medecin" or user_credentials.get("role") == "admin"):
        print("6 : Consulter la liste de suivi mes citoyens")
    if (user_credentials.get("role") == "medecin" ):
        print("7 : Mettre à jour le status d'un patient")
        print("8 : Suivre le status d'un patient un patient")
    if (user_credentials.get("role") == "admin" ):
        print("9 : Suivre tous les  contacts")
        print("12 : Supprimer un compte")
    print("10 : Passer en mode écoute des changement d'état")
    print("11 : AFFICHER LES REGLES EN CAS SUSPICION")

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
        device = input("Entrer le nom du citoyen à tracker")
        request = requests.get("https://zlmz36.internetofthings.ibmcloud.com/api/v0002/device/types/DTC/devices/"+device+"/events", headers=headers, auth=(api_key, api_token))

        if(request.status_code):
            response_array = request.json()
            i=0
            for dict in response_array:
                for key in dict:
                    if(dict["eventId"] == "contact"):
                        i = i +1
                        content = dict["payload"]
                        print("Le citoyen à été en contact avec : %s" % (base64.b64decode(content).decode('utf-8')))
            print("Nombre de contact du citoyen :"+ str(i))
        else:
            print("Citoyen  invalide")
    if options == 7:
        MedicalUpdateStatus()
    if options == 9:
        AdminSubscribeToAll()
    if options == 8:
        contact(input("Entrer l'ID du citoyen à suivre"))
    if options == 10:
        print("afficher tt les publish auquel le user est sub")
    if options == 11:
        print("Jai des symptômes (toux, fièvre) qui me font penser au COVID-19 je reste à domicile, jévite les contacts, jappelle un médecin avant de me rendre à son cabinet ou jappelle le numéro de permanence de soins de ma région. Je peux également bénéficier dune téléconsultation "
              "si les symptômes saggravent avec des difficultés respiratoires et signes détouffement, jappelle le SAMU (15) ou jenvoie un message au numéro durgence pour les sourds et malentendants (114).")
        print("\n       -Les principaux symptômes :")
        print("\n       -fièvre")
        print("\n       -toux")
        print("\n       -fatigue inhabituelle")
        print("\n       -difficultés respiratoires, étouffements")
        print("\n       -maux de tête")
        print("\n       -perte de goût et de lodorat")
        print("\n       -courbatures")
        print("\n       -parfois diarrhées")
        time.sleep(5)
    if options == 12:
        name_device = input("Taper le nom du device à supprimer")
        deleteDevice(name_device)

client.disconnect()