from fastapi import FastAPI
from ScreenController import ScreenController
import threading

screen_controller = ScreenController()
thread = threading.Thread(target=screen_controller.start)
thread.daemon = True
thread.start()

app = FastAPI()



@app.get('/')
def hello_world():
    screen_controller.next_slide()
    return {"Hello": "World!"}


