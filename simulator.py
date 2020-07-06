import os
import asyncio
import time
import random
from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient

# Define the JSON message to send to the IoT Hub
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_JSON = '{{"temperature":{temperature}, "humidity":{humidity}}}'

def iothub_client_init():
    # Fetch the connection string from an enviornment variable
    CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def generate_sample_message():
    temperature = TEMPERATURE + (random.random()*15)
    humidity = HUMIDITY + (random.random()*20)
    msg_body = MSG_JSON.format(temperature=temperature, humidity=humidity)
    return Message(msg_body)

async def send_telemetry_forever():
    try:
        client = iothub_client_init()
        await client.connect()
        while True:
            message = generate_sample_message()
            print(f"Sending message: {message}")
            await client.send_message(message)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopped by user control")
        await client.disconnect()
    except:
        print("Unexpected operation happend")
        await client.disconnect()


if __name__ == "__main__":
    print("Start IoT Hub simulator")
    asyncio.run(send_telemetry_forever())