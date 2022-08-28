
from fastapi.testclient import TestClient
from main import app
from faker import Faker
from typing import List
from models import Visiter
from sqlmodel import Session,select
from database import create_db_and_tables,engine

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

def test_create_visiter_with_invalid_body():
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


def test_read_visiter():
    response = client.get('/')
    data = response.json()
    # Check status code 
    assert response.status_code == 200

    # Check body 
    create_db_and_tables()
    db = []
    with Session(engine) as session:
        db = session.exec(select(Visiter)).all()
    assert len(db) == len(data)
    for i in range(len(db)):
        db_obj = db[i]
        res_obj = Visiter(**data[i])
        assert db_obj.id == res_obj.id
        assert db_obj.ipv6 == res_obj.ipv6
        assert db_obj.action == res_obj.action
        assert db_obj.chrome == res_obj.chrome
        assert db_obj.mac_address == res_obj.mac_address
        assert db_obj.port_number == res_obj.port_number
        assert db_obj.timezone == res_obj.timezone

def test_read_one_visiter():
    id = 2
    res = client.get(f'/{id}')
    data = res.json()

    # Check status code 
    assert res.status_code == 200

    # Check data 
    db_obj = {}
    with Session(engine) as session:
        db_obj = session.get(Visiter,id)
    res_obj = Visiter(**data)
    assert db_obj.id == res_obj.id
    assert db_obj.ipv6 == res_obj.ipv6
    assert db_obj.action == res_obj.action
    assert db_obj.chrome == res_obj.chrome
    assert db_obj.mac_address == res_obj.mac_address
    assert db_obj.port_number == res_obj.port_number
    assert db_obj.timezone == res_obj.timezone

def test_read_one_visiter_not_exist():
    id = 50
    res = client.get(f'/{id}')
    data = res.json()

    # Check status code 
    assert res.status_code == 404

def test_update_visior():
    id = 2
    res_body = {
        'ipv6':fake.ipv6(),
        'chrome':fake.chrome(),
    }
    res = client.put(url=f"/{id}",json=res_body)
    data = res.json()
    # Check Status Code 
    assert res.status_code == 202
    # Check Response Body 
    with Session(engine) as session:
        visitorInDb = session.get(Visiter,id)
        visitorInDbDict = visitorInDb.__dict__
        for k in data.keys():
            if k in ['ipv6', 'mac_address', 'chrome', 'action', 'port_number', 'id', 'timezone']:
                assert data[k] == visitorInDbDict[k]

def test_update_visior_not_exist():
    id = 20
    res_body = {
        'ipv6':fake.ipv6(),
        'chrome':fake.chrome(),
    }
    res = client.put(url=f"/{id}",json=res_body)
    data = res.json()
    # Check Status Code 
    assert res.status_code == 404

def test_update_visior_invalid_body():
    id = 20
    res_body = {
        'ipv6':fake.ipv6(),
        'port_number':"Text",
    }
    res = client.put(url=f"/{id}",json=res_body)
    data = res.json()
    # Check Status Code 
    assert res.status_code == 422