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

@bp.route('/<int:student_id>', methods=['OPTIONS','GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'StudentID': student.StudentID,
        'Name': student.Name,
        'DateOfBirth': student.DateOfBirth.isoformat(),
        'Address': student.Address
    })

@bp.route('/<int:student_id>', methods=['OPTIONS','PUT'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    student.Name = data['Name']
    student.DateOfBirth = data['DateOfBirth']
    student.Address = data['Address']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@bp.route('/<int:student_id>', methods=['OPTIONS','DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})