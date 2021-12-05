from fastapi import FastAPI, Depends, Header, HTTPException, status, Request
from typing import List
from app.entities.network_device import NetworkDevice
from app.persistence import Persistence
from typing import Optional
import os

app = FastAPI()
file_persistence = Persistence()


def get_persistence():
    return file_persistence


def GET_API_TOKEN():
    return os.environ.get('API_TOKEN', 'SECRET_TOKEN')


def api_token(api_token: Optional[str] = Header(...)):
    if not api_token or api_token != GET_API_TOKEN():
        raise HTTPException(status.HTTP_403_FORBIDDEN)


@app.on_event("shutdown")
async def on_shutdown():
    get_persistence().shutdown()


@app.post("/api/network-devices", dependencies=[Depends(api_token)])
async def create_network_device(network_device: NetworkDevice, request: Request,
                                persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    return persistence.persist(network_device)


@app.put("/api/network-devices/{fqdn}/", dependencies=[Depends(api_token)])
async def update_network_device(fqdn: str, network_device: NetworkDevice,
                                persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    return persistence.update(fqdn, network_device)


@app.get("/api/network-devices/{fqdn}/", dependencies=[Depends(api_token)])
async def get_network_device(fqdn: str,
                             persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    return persistence.find_by_fqdn(fqdn)


@app.get("/api/network-devices", dependencies=[Depends(api_token)])
async def get_network_devices(persistence: Persistence = Depends(get_persistence())) -> List:
    return persistence.find_all()


@app.delete("/api/network-devices/{fqdn}/", dependencies=[Depends(api_token)])
async def update_network_device(fqdn: str,
                                persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    return persistence.delete(fqdn)
