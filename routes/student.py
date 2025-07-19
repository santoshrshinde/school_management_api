from flask import Blueprint, jsonify, request
from models import Student
from extensions import db

bp = Blueprint('student', __name__, url_prefix='/students')

@bp.route('/', methods=['OPTIONS','GET'])
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

@bp.route('/', methods=['OPTIONS','GET', 'POST'])
def add_student():
    print('aading student')
    # data = request.get_json()
    # print('data')
    # print(data)
    # new_student = Student(
    #     Name=data['Name'],
    #     DateOfBirth=data['DateOfBirth'],
    #     Address=data['Address']
    # )
    # print(new_student)
    # db.session.add(new_student)
    # db.session.commit()
    # return jsonify({'message': 'Student added successfully'})

    data = request.json
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'}), 201
