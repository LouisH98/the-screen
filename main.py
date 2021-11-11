from fastapi import FastAPI
from ScreenController import ScreenController
import multiprocessing
from multiprocessing.connection import Listener, Client

listener = multiprocessing.connection.Listener(('localhost', 6000), authkey=b'the-screen')

thread = multiprocessing.Process(target=ScreenController().start)
thread.start()

client_conn = listener.accept()

app = FastAPI()

client_conn.send('init-parent')
client = Client(('localhost', 6001), authkey=b'the-screen')
print("Got client")



@app.get('/next-slide')
def hello_world():
    # ask for next slide
    client_conn.send("next_slide")

    # get name of new slide
    new_slide = client.recv()
    return {"status": "successful", "new_slide": new_slide}

@app.put('/brightness/')
def set_brightness(value=0.5):
    try:
        value = float(value)
    except:
        return {"status": "error", "message": "Invalid parameter: must be a number"}

    if value > 1 or value < 0.1:
        return {"status": "error", "message": "Invalid parameter: value must be less than 1 and greater than 0"}

    client_conn.send(f'set_brightness {value}')
    return {"status": "successful"}

@app.get('/status')
def get_status():
    client_conn.send("get_status")
    status = client.recv()
    return status
