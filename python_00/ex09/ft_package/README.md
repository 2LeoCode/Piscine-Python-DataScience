TCPIO: A Lightweight TCP library based on event driven I/O.

### Server example ###
```python
from tcpio import Server

server = Server("0.0.0.0:3000")
EMERGENCY_SHUTDOWN_CODE = "I love TCPIO!"
SERVER_PASSWORD = "I hate TCPIO!"


@server.on
def connection(client: Server.Client):
    print(f"New connection from {client.addr}")

    @client.on
    def ping(data: str):
        print(f"Received a ping request from {client.addr}: {data}")
        client.emit("pong", data)

    @client.once
    def emergency_shutdown(code: str):
        if code == EMERGENCY_SHUTDOWN_CODE:
            print(f"WARNING: Emergency shutdown requested by {client.addr}!")
            server.stop()
        else:
            print(f"WARNING: {client.addr} is an intruder! Exterminate!")
            client.disconnect()

    def login_event(password: str):
        print(f"Login with {password}")
        logged_in = False
        if password == SERVER_PASSWORD:
            print(f"{client.addr} logged in successfully!")

            @client.on
            def get_emergency_shutdown_code():
                print(
                    "Sending emergency shutdown code "
                    f"to authorized client {client.addr}"
                )
                client.emit("emergency_shutdown_code", EMERGENCY_SHUTDOWN_CODE)
            logged_in = True
        client.emit("login", logged_in)

    client.on("login", login_event)
    client.emit("welcome")


@server.on
def some_global_event(
        client: Server.Client,
        some_data: str,
        some_trigger: bool = False,
):
    print(f"Received some data: {some_data} from {client.addr}")
    if some_trigger:
        print("Some trigger was triggered... But nothing happened.")
        client.emit("sorry dude, nothing happened")


@server.on
def disconnection(client: Server.Client):
    print(f"Client {client.addr} disconnected, goodbye!")


@server.on
def error(error: Exception):
    print(f"Oops, something went wrong: {error}")


server.start(block=True)
```

### Client example ### 
```python
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
```
