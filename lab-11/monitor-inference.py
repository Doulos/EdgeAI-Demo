import paho.mqtt.client as mqtt
import datetime
import time

import paho.mqtt.subscribe as subscribe

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("clock/detected")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))


# Broker for prototyping MQTT communications

broker_address = "test.mosquitto.org"

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message


client.connect(broker_address,1883,60)

now = datetime.datetime.now()
time_stamp = str(now)

print("Current date and time: ", time_stamp)

client.loop_forever()

while True:
    client.subscribe("clock/detected")
    time.sleep(1)

