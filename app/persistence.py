import pickle
import os
from typing import List

from pydantic import BaseModel
from fastapi import HTTPException, status
from pydantic.tools import parse_obj_as

from app.entities.network_device import NetworkDevice


class Persistence():
    data = {}

    def DATA_FILE(self):
        return os.environ.get('STORAGE_DIR', '/tmp') + '/network_devices.pickle'

    def __init__(self):
        print("INIT")
        try:
            with open(self.DATA_FILE(), 'rb') as handle:
                self.data = pickle.load(handle)
            print("Finished data load")
        except Exception as e:
            print('Failed loading data!')

    def __call__(self):
        return self

    def shutdown(self):
        print("SHUTDOWN")
        with open(self.DATA_FILE(), 'wb') as handle:
            pickle.dump(self.data, handle)

    def find_by_fqdn(self, fqdn: str):
        try:
            return self.data[fqdn]
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def find_all(self):
        return parse_obj_as(List[NetworkDevice], list(self.data.values()))

    def persist(self, obj: BaseModel):
        if obj.fqdn in self.data.keys():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Entity exists!")
        self.data[obj.fqdn] = obj.dict()
        return obj

    def update(self, fqdn, network_device: BaseModel):
        self.data[fqdn] = network_device
        return network_device

    def delete(self, fqdn):
        print(f"{fqdn} {self.data.keys()}")
        try:
            return self.data.pop(fqdn)
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
