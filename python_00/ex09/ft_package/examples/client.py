from tcpio import Client
from time import sleep

client = Client("localhost:3000")


@client.on
def login(success: bool):
    if success:
        print("Successfully logged in to server!")

        @client.once
        def emergency_shutdown_code(code: str):
            print(f"Received emergency shutdown code from server: {code}")
            client.emit("emergency_shutdown", code)
        client.emit("get_emergency_shutdown_code")
    else:
        print("Failed to login to server!")


@client.on
def welcome():
    print("Received welcome from server!")


@client.once
def connect():
    print("Connected to server!")


client.emit("login", "some invalid password")
client.emit("emergency_shutdown", "some invalid code")


@client.on
def disconnect():
    print("Oops, you got disconnected!")


def reconnect():
    print("Trying to reconnect...")

    @client.once
    def connect():
        print("Reconnected to server!")

        def on_global_event_response():
            print("Nothing happened, what a shame!")
            print("Let's try to destroy everything then!")
            client.emit("login", "I hate TCPIO!")

        client.once("sorry dude, nothing happened", on_global_event_response)
        client.emit("some_global_event", "some data", some_trigger=True)
    sleep(2)
    client.connect()


client.once("disconnect", reconnect)


@client.on
def error(error: Exception):
    print(f"Oops, something went wrong: {error}")


client.connect()
