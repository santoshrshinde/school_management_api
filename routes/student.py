from flask import Blueprint, request, jsonify
from models import db, Student

bp = Blueprint('student', __name__, url_prefix='/students')

@bp.route('/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        'StudentID': s.StudentID,
        'Name': s.Name,
        'DateOfBirth': str(s.DateOfBirth),
        'Address': s.Address
    } for s in students])

@bp.route('/', methods=['POST'])
def add_student():
    data = request.json
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'}), 201