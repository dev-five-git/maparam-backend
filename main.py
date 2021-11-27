from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from v1 import v1_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/v1", tags=["v1"])


@app.get("/")
def root():
    return "maparam-api"


@app.get("/dummy/list")
def dummylist():
    return [{"testkey": "testvalue"}, {"testkey1": "testvalue1"}, {"testkey2": "testvalue2"},
            {"testkey3": "testvalue3"}, {"testkey4": "testvalue4"}, {"testkey5": "testvalue5"},
            {"testkey7": "testvalue2"}, {"testkey7": "testvalue7"}, {"testkey8": "testvalue8"},
            {"testkey9": "testvalue9"}, {"testkey10": "testvalue10"}, {"testkey11": "testvalue11"},
            {"testkey12": "testvalue12"}]


handler = Mangum(app=app)
