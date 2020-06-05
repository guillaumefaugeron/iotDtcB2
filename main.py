import json
import wiotp.sdk.application

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))


myConfig = wiotp.sdk.application.parseConfigFile("config.yaml")
client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)
client.deviceEventCallback = myEventCallback

client.commandCallback = myCommandCallback


client.connect()
client.subscribeToDeviceEvents(typeId="DTC",eventId="contact")

print(client.subscriptionCallback)
while 1:
    a=1

client.disconnect()
