import pickle
from typing import List

from pydantic import BaseModel
from fastapi import HTTPException, status
from pydantic.tools import parse_obj_as

from app.entities.network_device import NetworkDevice


class Persistence():
    data = {}

    def DATA_FILE(self):
        return '/tmp/network_devices.pickle'

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
        self.data[obj.fqdn] = obj.dict()
        return obj

    def update(self, fqdn, network_device: BaseModel):
        self.data[fqdn] = network_device
        return network_device
