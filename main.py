from this import s
from typing import List
import multiprocessing
from multiprocessing.connection import Listener, Client
import threading
import asyncio
from sse_starlette.sse import EventSourceResponse

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from response_types import StatusResponse
from ScreenController import ScreenController

listener = multiprocessing.connection.Listener(('localhost', 6000), authkey=b'the-screen')

thread = multiprocessing.Process(target=ScreenController(is_server=True).start)
thread.start()

client_conn = listener.accept()

app = FastAPI(
        title="The Screen - API",
        version="0.0.1"
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_conn.send('init-parent')
client = Client(('localhost', 6001), authkey=b'the-screen')
print("Got client")


lock = threading.Lock()

def send_message(message: str) -> str:
    if(not message):
         return
    lock.acquire()

    client_conn.send(message)

    message = client.recv()

    lock.release()

    return message


STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond
@app.get('/screen/stream')
async def message_stream(request: Request):
    # initialise a connection to the screen
    lock.acquire()
    client_conn.send('stream')
    stream_client =  Client(('localhost', 6005), authkey=b'stream-the-screen')
    lock.release()
    def new_messages():
        # Add logic here to check for new messages
        # maybe screen.poll()?
        yield stream_client.poll()
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                lock.acquire()
                client_conn.send('stop_stream')
                stream_client.close()
                lock.release()
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                data = stream_client.recv()
                print("got", data)
                yield {
                        "event": "new_message",
                        "id": "message_id",
                        "retry": RETRY_TIMEOUT,
                        "data": data
                }

            # await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.get('/next-slide', response_model=StatusResponse)
def next_slide():
    # ask for next slide
    return send_message("next_slide")

@app.put('/rotation', response_model=StatusResponse)
def set_rotation(value: int = 0):
    client_conn.send(f"set_rotation {value}")
    return send_message("get_status")

@app.put('/brightness', response_model=StatusResponse)
def set_brightness(value=0.5):
    try:
        value = float(value)
    except:
        return {"status": "error", "message": "Invalid parameter: must be a number"}

    if value > 1 or value < 0.1:
        return {"status": "error", "message": "Invalid parameter: value must be less than 1 and greater than 0"}
    client_conn.send(f'set_brightness {value}')
    return send_message("get_status")

@app.put('/auto-rotate', response_model=StatusResponse)
def set_autorotate(rotate: bool):
    try:
        value = bool(rotate)
    except: 
        return {"status": "error", "message": "Invalid parameter: must be a boolean value"}

    client_conn.send(f"set_auto_rotate {value}")
    new_value = client.recv()
    return send_message("get_status") 

@app.get('/slides')
def get_slides() -> List[str]:
    return send_message('get_slides')

@app.put('/slide') 
def set_slide(slide_name: str = Query(..., min_length=1)):
    current_slide = send_message(f'set_slide {slide_name}')

    if current_slide is None:
        return {"status": "ERROR", "message": f"Slide '{slide_name}' does not exist, try again with a different name"}

    return send_message("get_status") 

@app.get('/status', response_model=StatusResponse)
def get_status_endpoint():
    return send_message("get_status")
