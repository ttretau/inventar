from fastapi import FastAPI, Depends
from typing import List
from app.entities.network_device import NetworkDevice
from app.persistence import Persistence, persistence

app = FastAPI()

@app.get("/hello")
def hello():
    return {"hello": "world!"}


@app.post("/api/network-devices")
def create_network_device(network_device: NetworkDevice,
                          persistence: Persistence = Depends(persistence)) -> NetworkDevice:
    persistence.persist(network_device)
    return network_device


@app.put("/api/network-devices/{fqdn}/")
def update_network_device(fqdn: str, network_device: NetworkDevice,
                          persistence: Persistence = Depends(persistence)) -> NetworkDevice:
    persistence.update(fqdn, network_device)
    return network_device


@app.get("/api/network-devices/{fqdn}/")
def get_network_device(fqdn: str, persistence: Persistence = Depends(persistence)) -> NetworkDevice:
    return persistence.find_by_fqdn(fqdn)


@app.get("/api/network-devices")
def get_network_devices(persistence: Persistence = Depends(persistence)) -> List:
    return persistence.find_all()
