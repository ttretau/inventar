import pickle
from pydantic import BaseModel
from fastapi import HTTPException, status


class Persistence():

    def DATA_FILE(self):
        return '/tmp/network_devices.pickle'

    def __init__(self):
        global data
        try:
            print('open data')
            with open(self.DATA_FILE(), 'rb') as handle:
                data = pickle.load(handle)
            print("finished data load")
        except Exception as e:
            print('Failed loading data!')
            data = {}

    def __call__(self):
        return self

    def shutdown(self):
        with open(self.DATA_FILE(), 'wb') as handle:
            pickle.dump(data, handle)

    def find_by_fqdn(self, fqdn: str):
        try:
            return data[fqdn]
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def find_all(self):
        return []

    def persist(self, obj: BaseModel):
        data[obj.fqdn] = obj

    def update(self, fqdn, network_device: BaseModel):
        data[fqdn] = network_device


persistence = Persistence()
