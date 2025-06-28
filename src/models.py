from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Client(db.Model):  # type: ignore[name-defined]
    """
    Модель клиента.
    """

    __tablename__ = "client"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    credit_card = Column(String(50))
    car_number = Column(String(10))

    parking_logs = relationship("ClientParking", backref="client", lazy=True)


class Parking(db.Model):  # type: ignore[name-defined]
    """
    Модель парковки.
    """

    __tablename__ = "parking"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(100), nullable=False)
    opened = Column(Boolean)
    count_places = Column(Integer, nullable=False)
    count_available_places = Column(Integer, nullable=False)

    client_logs = relationship("ClientParking", backref="parking", lazy=True)


class ClientParking(db.Model):  # type: ignore[name-defined]
    """
    Модель связи клиента и парковки.
    """

    __tablename__ = "client_parking"

    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    parking_id = Column(Integer, ForeignKey("parking.id"), nullable=False)
    time_in = Column(DateTime, nullable=False)
    time_out = Column(DateTime, nullable=True)
    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )
