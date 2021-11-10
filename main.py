from fastapi import FastAPI
from ScreenController import ScreenController
import multiprocessing
from multiprocessing.connection import Listener, Client

listener = multiprocessing.connection.Listener(('localhost', 6000), authkey=b'the-screen')

thread = multiprocessing.Process(target=ScreenController().start)
thread.start()

conn = listener.accept()

app = FastAPI()

conn.send('init-parent')
client = Client(('localhost', 6001), authkey=b'the-screen')
print("Got client")



@app.get('/next-slide')
def hello_world():
    # ask for next slide
    conn.send("next_slide")

    # get name of new slide
    new_slide = client.recv()
    return {"status": "successful", "new_slide": new_slide}

@app.get('/status')
def get_status():
    conn.send("get_status")
    status = client.recv()
    return status
