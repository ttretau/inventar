from fastapi import FastAPI, Depends, Header, HTTPException, status, Request
from typing import List
from app.entities.network_device import NetworkDevice
from app.persistence import Persistence
from typing import Optional
import os

from app.persistence_mongo import PersistenceMongo

app = FastAPI()
file_persistence = Persistence()
mongo_persistence = PersistenceMongo(os.environ.get('MONGO_URL'))


def get_persistence():
    if os.environ.get('MONGO_URL') is not None:
        return mongo_persistence
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
async def create_network_device(network_device: NetworkDevice,
                                persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    await persistence.persist(network_device)
    return network_device


@app.put("/api/network-devices/{fqdn}/", dependencies=[Depends(api_token)])
async def update_network_device(fqdn: str, network_device: NetworkDevice,
                                persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    result = await persistence.update(fqdn, network_device)
    return result


@app.get("/api/network-devices/{fqdn}/", dependencies=[Depends(api_token)])
async def get_network_device(fqdn: str,
                             persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    result = await persistence.find_by_fqdn(fqdn)
    return result


@app.get("/api/network-devices", dependencies=[Depends(api_token)])
async def get_network_devices(persistence: Persistence = Depends(get_persistence())) -> List:
    result = await persistence.find_all()
    return result


@app.delete("/api/network-devices/{fqdn}/", dependencies=[Depends(api_token)])
async def update_network_device(fqdn: str,
                                persistence: Persistence = Depends(get_persistence())) -> NetworkDevice:
    result = await persistence.delete(fqdn)
    return result
