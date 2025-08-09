from flask import Blueprint, request, jsonify
from extensions import db
from models import StudentBus

bp = Blueprint('studentbus', __name__, url_prefix='/studentbus')

# Get all student-bus assignments
@bp.route('/', methods=['GET'])
def get_all_studentbus():
    studentbus_list = StudentBus.query.all()
    result = []
    for sb in studentbus_list:
        result.append({
            'StudentBusID': sb.StudentBusID,
            'StudentID': sb.StudentID,
            'BusID': sb.BusID
        })
    return jsonify(result)

# Add a new student-bus assignment
@bp.route('/', methods=['POST'])
def add_studentbus():
    data = request.get_json()
    new_sb = StudentBus(
        StudentID=data.get('StudentID'),
        BusID=data.get('BusID')
    )
    db.session.add(new_sb)
    db.session.commit()
    return jsonify({'message': 'Student-Bus record added successfully'}), 201

# Get a single student-bus assignment by ID
@bp.route('/<int:id>', methods=['GET'])
def get_studentbus(id):
    sb = StudentBus.query.get_or_404(id)
    return jsonify({
        'StudentBusID': sb.StudentBusID,
        'StudentID': sb.StudentID,
        'BusID': sb.BusID
    })

# Update student-bus assignment by ID
@bp.route('/<int:id>', methods=['PUT'])
def update_studentbus(id):
    sb = StudentBus.query.get_or_404(id)
    data = request.get_json()
    sb.StudentID = data.get('StudentID', sb.StudentID)
    sb.BusID = data.get('BusID', sb.BusID)
    db.session.commit()
    return jsonify({'message': 'Student-Bus record updated successfully'})

# Delete student-bus assignment by ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_studentbus(id):
    sb = StudentBus.query.get_or_404(id)
    db.session.delete(sb)
    db.session.commit()
    return jsonify({'message': 'Student-Bus record deleted successfully'})
