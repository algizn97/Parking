import pytest
from src.models import Client, Parking
from .factories import ClientFactory, ParkingFactory
from src import db, create_app

@pytest.mark.usefixtures('client')
def test_create_client_with_factory(client):

    client_data = ClientFactory()

    payload = {
        'name': client_data['name'],
        'surname': client_data['surname'],
        'credit_card': client_data['credit_card'],
        'car_number': client_data['car_number']
    }


    response = client.post('/clients', json=payload)
    assert response.status_code == 201

    created_id = response.get_json()['id']
    with create_app().app_context():
        db_client = db.session.get(Client, created_id)
        assert db_client is not None
        assert db_client.name == payload['name']
        assert db_client.surname == payload['surname']
        assert db_client.credit_card == payload['credit_card']
        assert db_client.car_number == payload['car_number']


@pytest.mark.usefixtures('client')
def test_create_parking_with_factory(client):

    parking_data = ParkingFactory()

    payload = {
        'address': parking_data['address'],
        'opened': parking_data['opened'],
        'count_places': parking_data['count_places'],
        'count_available_places': parking_data['count_available_places'],
    }

    response = client.post('/parkings', json=payload)
    assert response.status_code == 201

    created_id = response.get_json()['id']
    with create_app().app_context():
        db_parking = db.session.get(Parking, created_id)
        assert db_parking is not None
        assert db_parking.address == payload['address']
        assert db_parking.opened == payload['opened']
        assert db_parking.count_places == payload['count_places']
        assert db_parking.count_available_places == payload['count_available_places']
