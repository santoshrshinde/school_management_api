from flask import Blueprint, jsonify, request
from models import Student
from extensions import db

bp = Blueprint('student', __name__, url_prefix='/students')

@bp.route('/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([
        {
            'StudentID': s.StudentID,
            'Name': s.Name,
            'DateOfBirth': s.DateOfBirth.isoformat(),
            'Address': s.Address
        } for s in students
    ])

@bp.route('/', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        Name=data['Name'],
        DateOfBirth=data['DateOfBirth'],
        Address=data['Address']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'})
