from fastapi import FastAPI

from app.entities.network_device import NetworkDevice

app = FastAPI()


@app.get("/hello")
def hello():
    return {"hello": "world!"}


@app.post("/api/network-devices")
def create_device(network_device: NetworkDevice):
    return network_device
