import pytest
from datetime import datetime, timedelta, timezone


@pytest.fixture(scope='session')
def app():
    from src import create_app
    from src.models import db as _db
    from src.models import Client, Parking, ClientParking

    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        _db.create_all()

        client = Client(
            name='Test',
            surname='User',
            credit_card='1234-5678-9012-3456',
            car_number='A123BC'
        )
        _db.session.add(client)

        parking = Parking(
            address='Test Address',
            opened=True,
            count_places=10,
            count_available_places=10
        )
        _db.session.add(parking)
        _db.session.commit()

        time_in = datetime.now(timezone.utc) - timedelta(hours=1)
        time_out = datetime.now(timezone.utc)
        parking_log = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=time_in,
            time_out=time_out
        )
        _db.session.add(parking_log)
        _db.session.commit()

    yield app

    with app.app_context():
        _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    from __main__ import db as _db
    return _db
