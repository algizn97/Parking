import pytest
import uuid


@pytest.mark.parametrize("url", [
    "/clients",
    "/clients/1"
])
def test_get_methods_return_200(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client):
    data = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "А001АА77"
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_create_parking(client):
    data = {
        "address": "ул. Тестовая, 42",
        "count_places": 50,
        "count_available_places": 50
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    assert 'id' in response.get_json()


@pytest.mark.parking
def test_enter_parking(client):
    unique_id = uuid.uuid4().hex[:6]
    client_data = {
        "name": f"Петр-{unique_id}",
        "surname": f"Петров-{unique_id}"
    }
    response = client.post('/clients', json=client_data)
    assert response.status_code == 201, f"Ошибка создания клиента: {response.get_json()}"
    client_id = response.get_json()['id']

    parking_data = {
        "address": f"ул. Парковая-{unique_id}",
        "count_places": 20,
        "count_available_places": 20
    }
    response = client.post('/parkings', json=parking_data)
    assert response.status_code == 201, f"Ошибка создания парковки: {response.get_json()}"
    parking_id = response.get_json()['id']

    enter_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    response = client.post('/client_parkings', json=enter_data)
    assert response.status_code == 201


@pytest.mark.parking
def test_exit_parking(client):
    unique_id = uuid.uuid4().hex[:6]
    client_data = {
        "name": f"Сидор-{unique_id}",
        "surname": f"Сидоров-{unique_id}",
        "credit_card": "1111-2222-3333-4444"
    }
    response = client.post('/clients', json=client_data)
    assert response.status_code == 201, f"Ошибка создания клиента: {response.get_json()}"
    client_id = response.get_json()['id']

    parking_data = {
        "address": f"ул. Выездная-{unique_id}",
        "count_places": 30,
        "count_available_places": 30
    }
    response = client.post('/parkings', json=parking_data)
    assert response.status_code == 201, f"Ошибка создания парковки: {response.get_json()}"
    parking_id = response.get_json()['id']

    # Заезд
    enter_data = {"client_id": client_id, "parking_id": parking_id}
    response = client.post('/client_parkings', json=enter_data)
    assert response.status_code == 201

    # Выезд
    exit_data = {"client_id": client_id, "parking_id": parking_id}
    response = client.delete('/client_parkings', json=exit_data)
    assert response.status_code == 200
