from . import db


class Client(db.Model):
    """
    Модель клиента.
    """
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    parking_logs = db.relationship('ClientParking', backref='client', lazy=True)


class Parking(db.Model):
    """
    Модель парковки.
    """
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_logs = db.relationship('ClientParking', backref='parking', lazy=True)


class ClientParking(db.Model):
    """
    Модель связи клиента и парковки.
    """
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)
    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )
