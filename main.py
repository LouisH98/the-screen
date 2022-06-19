from fastapi import FastAPI, Query
from ScreenController import ScreenController
import multiprocessing
from multiprocessing.connection import Listener, Client
from typing import List
from response_types import StatusResponse

listener = multiprocessing.connection.Listener(('localhost', 6000), authkey=b'the-screen')

thread = multiprocessing.Process(target=ScreenController(is_server=True).start)
thread.start()

client_conn = listener.accept()

app = FastAPI(
        title="The Screen - API",
        version="0.0.1"
        )

client_conn.send('init-parent')
client = Client(('localhost', 6001), authkey=b'the-screen')
print("Got client")

def get_status():
    client_conn.send('get_status')
    return client.recv()

@app.get('/next-slide', response_model=StatusResponse)
def next_slide():
    # ask for next slide
    client_conn.send("next_slide")
    return get_status()

@app.put('/rotation', response_model=StatusResponse)
def set_rotation(value: int = 0):
    client_conn.send(f"set_rotation {value}")
    return get_status()

@app.put('/brightness', response_model=StatusResponse)
def set_brightness(value=0.5):
    try:
        value = float(value)
    except:
        return {"status": "error", "message": "Invalid parameter: must be a number"}

    if value > 1 or value < 0.1:
        return {"status": "error", "message": "Invalid parameter: value must be less than 1 and greater than 0"}
    client_conn.send(f'set_brightness {value}')
    return get_status()

@app.put('/auto-rotate', response_model=StatusResponse)
def set_autorotate(rotate: bool):
    try:
        value = bool(rotate)
    except: 
        return {"status": "error", "message": "Invalid parameter: must be a boolean value"}

    client_conn.send(f"set_auto_rotate {value}")
    new_value = client.recv()
    return get_status() 

@app.get('/slides')
def get_slides() -> List[str]:
    client_conn.send('get_slides')
    slides = client.recv()
    return slides

@app.put('/slide') 
def set_slide(slide_name: str = Query(..., min_length=1)):
    client_conn.send(f'set_slide {slide_name}')
    current_slide = client.recv()

    if current_slide is None:
        return {"status": "ERROR", "message": f"Slide '{slide_name}' does not exist, try again with a different name"}

    return get_status() 

@app.get('/status', response_model=StatusResponse)
def get_status_endpoint():
    return get_status()
