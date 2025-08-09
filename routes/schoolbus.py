from flask import Blueprint, jsonify, request
from models import SchoolBus
from extensions import db

bp = Blueprint('schoolbus', __name__, url_prefix='/schoolbus')

# Get all school buses
@bp.route('/', methods=['OPTIONS', 'GET'])
def get_schoolbuses():
    buses = SchoolBus.query.all()
    return jsonify([
        {
            'BusID': bus.BusID,
            'BusNumber': bus.BusNumber,
            'Driver': bus.Driver
        }
        for bus in buses
    ])

# Add a new school bus
@bp.route('/', methods=['OPTIONS', 'POST'])
def add_schoolbus():
    data = request.get_json()
    new_bus = SchoolBus(**data)
    db.session.add(new_bus)
    db.session.commit()
    return jsonify({'message': 'School bus added successfully'}), 201

# Get a single school bus by ID
@bp.route('/<int:bus_id>', methods=['OPTIONS', 'GET'])
def get_schoolbus(bus_id):
    bus = SchoolBus.query.get_or_404(bus_id)
    return jsonify({
        'BusID': bus.BusID,
        'BusNumber': bus.BusNumber,
        'Driver': bus.Driver
    })

# Update a school bus by ID
@bp.route('/<int:bus_id>', methods=['OPTIONS', 'PUT'])
def update_schoolbus(bus_id):
    bus = SchoolBus.query.get_or_404(bus_id)
    data = request.get_json()
    bus.BusNumber = data['BusNumber']
    bus.Driver = data['Driver']
    db.session.commit()
    return jsonify({'message': 'School bus updated successfully'})

# Delete a school bus by ID
@bp.route('/<int:bus_id>', methods=['OPTIONS', 'DELETE'])
def delete_schoolbus(bus_id):
    bus = SchoolBus.query.get_or_404(bus_id)
    db.session.delete(bus)
    db.session.commit()
    return jsonify({'message': 'School bus deleted successfully'})
