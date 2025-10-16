#!/usr/bin/env python3
import json
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "ucla/180da/skye/demo"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    # Subscribe on connect so it re-subscribes after reconnects
    client.subscribe(TOPIC, qos=1)

def on_disconnect(client, userdata, rc):
    print("Expected Disconnect" if rc == 0 else "Unexpected Disconnect")

def on_message(client, userdata, message):
    payload = message.payload
    try:
        # Try JSON first
        decoded = json.loads(payload.decode("utf-8"))
    except Exception:
        decoded = payload.decode("utf-8", errors="replace")
    print(f'Received on "{message.topic}" (QoS {message.qos}): {decoded}')

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
