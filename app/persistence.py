import pickle
from pydantic import BaseModel
from fastapi import HTTPException, status


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
        return []

    def persist(self, obj: BaseModel):
        self.data[obj.fqdn] = obj.dict()
        return obj

    def update(self, fqdn, network_device: BaseModel):
        self.data[fqdn] = network_device
