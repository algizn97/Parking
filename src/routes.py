from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from .models import Client, ClientParking, Parking, db

bp = Blueprint("routes", __name__)


@bp.route("/clients", methods=["GET"])
def get_clients():
    """Получить список всех клиентов"""
    try:
        clients = Client.query.all()
        result = []
        for client in clients:
            result.append(
                {
                    "id": client.id,
                    "name": client.name,
                    "surname": client.surname,
                    "credit_card": client.credit_card,
                    "car_number": client.car_number,
                }
            )
        return jsonify(result)
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    """Получить клиента по ID"""
    try:
        client = Client.query.get_or_404(client_id)
        return jsonify(
            {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "credit_card": client.credit_card,
                "car_number": client.car_number,
            }
        )
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route("/clients", methods=["POST"])
def create_client():
    """Создать нового клиента"""
    data = request.get_json()
    try:
        if "name" not in data or "surname" not in data:
            return jsonify({"error": "Name and surname are required"}), 400

        client = Client(
            name=data["name"],
            surname=data["surname"],
            credit_card=data.get("credit_card"),
            car_number=data.get("car_number"),
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({"id": client.id}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route("/parkings", methods=["POST"])
def create_parking():
    """Создать новую парковку"""
    data = request.get_json()
    try:
        required_fields = ["address", "count_places", "count_available_places"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"})

        parking = Parking(
            address=data["address"],
            opened=data.get("opened", True),
            count_places=data["count_places"],
            count_available_places=data["count_available_places"],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({"id": parking.id}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route("/client_parkings", methods=["POST"])
def enter_parking():
    """Заезд на парковку"""
    data = request.get_json()
    if not data or "client_id" not in data or "parking_id" not in data:
        return jsonify({"error": "client_id и parking_id обязательны"}), 400

    client_id = data["client_id"]
    parking_id = data["parking_id"]
    parking = Parking.query.get_or_404(parking_id)

    if not parking.opened:
        return jsonify({"error": "Парковка закрыта"}), 400
    if parking.count_available_places <= 0:
        return jsonify({"error": "Нет свободных мест"}), 400

    existing_entry = ClientParking.query.filter_by(
        client_id=client_id, parking_id=parking_id, time_out=None
    ).first()
    if existing_entry:
        return jsonify({"error": "Клиент уже на парковке"}), 400

    try:
        log_entry = ClientParking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=datetime.now(timezone.utc),
        )
        parking.count_available_places -= 1
        db.session.add(log_entry)
        db.session.commit()
        return jsonify({"id": log_entry.id}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@bp.route("/client_parkings", methods=["DELETE"])
def exit_parking():
    """Выезд с парковки"""
    data = request.get_json()
    if not data or "client_id" not in data or "parking_id" not in data:
        return jsonify({"error": "client_id и parking_id обязательны"}), 400
    client_id = data["client_id"]
    parking_id = data["parking_id"]

    log_entry = ClientParking.query.filter(
        ClientParking.client_id == client_id,
        ClientParking.parking_id == parking_id,
        ClientParking.time_out.is_(None),
    ).first_or_404()

    client = Client.query.get_or_404(client_id)
    if not client.credit_card:
        return jsonify({"error": "У клиента нет привязанной карты"}), 400

    log_entry.time_out = datetime.now(timezone.utc)

    parking = Parking.query.get_or_404(parking_id)
    parking.count_available_places += 1

    db.session.commit()
    return jsonify({"success": "Выезд зарегистрирован"}), 200
