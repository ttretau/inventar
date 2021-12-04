from pydantic import BaseModel
from enum import Enum


class ModelType(str, Enum):
    IOS_XR = 'ios-xr'
    IOS_XE = 'ios-xe'
    NX_OS = 'nx-os'


class NetworkDevice(BaseModel):
    fqdn: str
    model: ModelType
    version = 'unknown'
