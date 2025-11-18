from flask import Blueprint, request, jsonify
from extensions import db
from models import StudentBus, Student, SchoolBus

bp = Blueprint('studentbus', __name__, url_prefix='/studentbus')

# ✅ Get all student-bus assignments
@bp.route('/', methods=['GET'])
def get_all_studentbus():
    results = (
        db.session.query(
            StudentBus.StudentBusID,
            Student.Name.label("StudentName"),
            SchoolBus.BusNumber.label("BusNumber"),
            StudentBus.StudentID,
            StudentBus.BusID
        )
        .join(Student, StudentBus.StudentID == Student.StudentID)
        .join(SchoolBus, StudentBus.BusID == SchoolBus.BusID)
        .all()
    )
    return jsonify([{
        "StudentBusID": sb.StudentBusID,
        "StudentID": sb.StudentID,
        "BusID": sb.BusID,
        "StudentName": sb.StudentName,
        "BusNumber": sb.BusNumber
    } for sb in results])

# ✅ Get all buses
@bp.route('/buses', methods=['GET'])
def get_buses():
    buses = SchoolBus.query.all()
    return jsonify([{"BusID": b.BusID, "BusNumber": b.BusNumber} for b in buses])

# ✅ Get all students
@bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{"StudentID": s.StudentID, "Name": s.Name} for s in students])

# ✅ Add new studentbus
@bp.route('/', methods=['POST'])
def add_studentbus():
    data = request.get_json()
    new_sb = StudentBus(StudentID=data.get('StudentID'), BusID=data.get('BusID'))
    db.session.add(new_sb)
    db.session.commit()
    return jsonify({'message': 'StudentBus added successfully'}), 201

# ✅ Get single studentbus
@bp.route('/<int:id>', methods=['GET'])
def get_studentbus(id):
    sb = StudentBus.query.get_or_404(id)
    return jsonify({
        "StudentBusID": sb.StudentBusID,
        "StudentID": sb.StudentID,
        "BusID": sb.BusID
    })

# ✅ Update studentbus
@bp.route('/<int:id>', methods=['PUT'])
def update_studentbus(id):
    sb = StudentBus.query.get_or_404(id)
    data = request.get_json()
    sb.StudentID = data.get('StudentID', sb.StudentID)
    sb.BusID = data.get('BusID', sb.BusID)
    db.session.commit()
    return jsonify({'message': 'StudentBus updated successfully'})

# ✅ Delete studentbus
@bp.route('/<int:id>', methods=['DELETE'])
def delete_studentbus(id):
    sb = StudentBus.query.get_or_404(id)
    db.session.delete(sb)
    db.session.commit()
    return jsonify({'message': 'StudentBus deleted successfully'})
