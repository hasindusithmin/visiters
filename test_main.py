
from fastapi.testclient import TestClient
from main import app
from faker import Faker



fake = Faker()
client = TestClient(app)

def test_create_visiter():

    body = {
        'ipv6':fake.ipv6(),
        'chrome':fake.chrome(),
        'port_number':fake.port_number(),
        'mac_address':fake.mac_address(),
        'timezone':fake.timezone(),
        'action':fake.text()
    }
    response = client.post(url="/",json=body)
    data = response.json()

    # Check status code
    assert response.status_code == 201
    # Check response body 
    for k in data.keys():
        if k == 'id':
            continue
        assert data[k] == body[k]

def test_create_visiter_with_invalid_data():
    body = {
        'ipv6':fake.ipv6(),
        'chrome':fake.chrome(),
        'port_number':'port_number',
        'mac_address':fake.mac_address(),
        'timezone':fake.timezone(),
        'action':fake.text()
    }
    response = client.post(url='/',json=body)

    assert response.status_code == 422

