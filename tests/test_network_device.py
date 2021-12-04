from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

test_request_device1 = {
    "fqdn": "device1.t0n.eu",
    "model": "ios-xr",
    "version": "11.0"
}

test_request_device2 = {
    "fqdn": "device2.fqdn.withlongerdomainname.eu",
    "model": "ios-xe",
    "version": "1.0"
}

test_request_update_device1 = {
    "fqdn": "device2.fqdn.eu",
    "model": "nx-os",
    "version": "12.0"
}


def test_create_network_device():
    response = client.post("/api/network-devices", json=test_request_device1)
    assert response.status_code == 200
    assert response.json() == test_request_device1


def test_create_another_network_device():
    response = client.post("/api/network-devices", json=test_request_device2)
    assert response.status_code == 200
    assert response.json() == test_request_device2


def test_get_network_device():
    response = client.get("/api/network-devices/device1%2et0n%2eeu/")
    assert response.status_code == 200
    assert response.json() == test_request_device1


def test_update_network():
    response = client.put("/api/network-devices/device1%2et0n%2eeu/", json=test_request_update_device1)
    assert response.status_code == 200

    response = client.get("/api/network-devices/device1%2et0n%2eeu/")
    assert response.status_code == 200
    assert response.json() == test_request_update_device1


def test_read_network_device_list():
    response = client.get("/api/network-devices")
    assert response.status_code == 200
    assert len(response.json()) > 1
