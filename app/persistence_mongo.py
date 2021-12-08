from http import HTTPStatus
from pydantic import BaseModel
from fastapi import HTTPException, status, Response
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
from app.entities.network_device import NetworkDevice


class PersistenceMongo():

    def __init__(self, mongo_url):
        print(f"INIT MONGO: {mongo_url}")
        if mongo_url is not None:
            self.client = AsyncIOMotorClient(mongo_url.replace('"', ''))
            self.database = self.client.inventar
            self.network_device_collection = self.database.get_collection("network_device_collection")

    def __call__(self):
        return self

    def shutdown(self):
        print("SHUTDOWN")

    async def find_by_fqdn(self, fqdn: str):
        if (network_device := await self.network_device_collection.find_one({"fqdn": fqdn})) is not None:
            result = NetworkDevice.parse_obj(network_device)
            return result

        raise HTTPException(status_code=404, detail=f"Device {fqdn} not found")

    async def find_all(self):
        result = []
        network_devices = await self.network_device_collection.find().to_list(length=None)
        for device in network_devices:
            result.append(NetworkDevice.parse_obj(device))
        return result

    async def persist(self, device: BaseModel):
        obj_data = jsonable_encoder(device)
        if (db_device := await self.network_device_collection.find_one({"fqdn": device.fqdn})) is not None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Entity {device.fqdn} exists!")
        await self.network_device_collection.insert_one(obj_data)
        return db_device

    async def update(self, fqdn, device: BaseModel):
        obj_data = jsonable_encoder(device)
        if (network_device := await self.network_device_collection.find_one({"fqdn": fqdn})) is not None:
            update_result = await self.network_device_collection.update_one({"_id": network_device._id},
                                                                            {"$set": obj_data})
            return update_result

        raise HTTPException(status_code=404, detail=f"Device {fqdn} not found")

    async def delete(self, fqdn):
        if (network_device := await self.network_device_collection.find_one({"fqdn": fqdn})) is not None:
            result = await self.network_device_collection.delete_one({"_id": network_device['_id']})
            if result.deleted_count == 1:
                return Response(status_code=HTTPStatus.NO_CONTENT.value)

        raise HTTPException(status_code=404, detail=f"Device {fqdn} not found")
