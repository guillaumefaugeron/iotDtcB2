import json
import wiotp.sdk.application

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))


# Subrcribe to all DTC devices
def AdminSubscribeToAll():
    print("Subscribing to all DTC devices...")
    client.subscribeToDeviceEvents(typeId="DTC",eventId="CitizenStatus")

myConfig = wiotp.sdk.application.parseConfigFile("default-config.yaml")
client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)
client.deviceEventCallback = myEventCallback

client.commandCallback = myCommandCallback


client.connect()
AdminSubscribeToAll()

print(client.subscriptionCallback)
while 1:
    a=1

client.disconnect()
