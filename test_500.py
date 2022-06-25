from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from time import sleep
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
@app.get('/test')
def test():
    return {"test": "test"}

@app.get('/test_sync')
def test_sync():
    sleep(1)
    return {"test": "test"}

    