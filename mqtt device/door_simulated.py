# Import necessary libraries
import paho.mqtt.client as mqtt
import time


topic = "teds20/group05/project"  # Topic where messages are published
broker_address = "test.mosquitto.org"  # Server where messages are published

people_inside = 15
print("People inside:", people_inside)
max_allowed = 20

# This function handles received messages


def on_message(client, userdata, message):
    received_msg = message.payload.decode('utf-8')

    # Stop program in case a STOP-string is sent
    if received_msg == "STOP":

        print("Unsubscribing from topic:", topic)
        client.unsubscribe(topic)  # unsubscribe

        # wait 4 seconds in order to ensure that we process every message.
        time.sleep(4)
        client.loop_stop()  # stop the event processing loop

        print("\ndisconnecting from broker")
        client.disconnect()  # disconnect from broker

    # If the message is not a STOP-string, send the message to the door_state function.
    else:
        door_state(received_msg)

# This function runs the logic of the simulated door. It allows a maximum of 20 people inside at any time.
# If anyone tries to enter when there are already 20 people inside, they are asked to wait until someone leaves.


def door_state(message):

    print("received message:", message)
    global people_inside

    if people_inside < max_allowed:
        if message == "IN":
            people_inside += 1
        if message == "OUT":
            # Bug handling for simulation purposes. make sure the counter does not go below zero. Can't be -1 person in a room.
            if people_inside > 0:
                people_inside -= 1
    else:
        if message == "IN":
            print(
                "Maximum number of people inside, please wait until someone leaves before entering")
        if message == "OUT":
            people_inside -= 1
    print("People inside:", people_inside)


client = mqtt.Client("P2")     # Create new instance.
client.on_message = on_message  # Specify the on_message function.


# Connect to the mqtt client.
try:
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker.
    client.subscribe(topic, 2)  # subscribe to the specified topic.
    print("Subscribing to topic:", topic)
    # start the event processing loop, this loop is terminated if a STOP-string is received in on_message.
    client.loop_forever()

except Exception as e:
    # if we receive an exception (error) in the "try" block,
    # handle it here, by printing out the error message
    print(f"connection error: {e}")
