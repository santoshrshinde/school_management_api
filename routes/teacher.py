from flask import Blueprint, jsonify, request
from models import Teacher
from extensions import db

bp = Blueprint('teacher', __name__, url_prefix='/teachers')

# Get all teachers
@bp.route('/', methods=['OPTIONS', 'GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([{
        'TeacherID': t.TeacherID,
        'Name': t.Name,
        'Subject': t.Subject,
        'Contact': t.Contact
    } for t in teachers])

# Add a new teacher
@bp.route('/', methods=['OPTIONS', 'POST'])
def add_teacher():
    data = request.get_json()
    new_teacher = Teacher(
        Name=data['Name'],
        Subject=data['Subject'],
        Contact=data['Contact']
    )
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher added successfully'}), 201

# Get a specific teacher by ID
@bp.route('/<int:teacher_id>', methods=['OPTIONS', 'GET'])
def get_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return jsonify({
        'TeacherID': teacher.TeacherID,
        'Name': teacher.Name,
        'Subject': teacher.Subject,
        'Contact': teacher.Contact
    })

# Update a teacher by ID
@bp.route('/<int:teacher_id>', methods=['OPTIONS', 'PUT'])
def update_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    data = request.get_json()
    teacher.Name = data['Name']
    teacher.Subject = data['Subject']
    teacher.Contact = data['Contact']
    db.session.commit()
    return jsonify({'message': 'Teacher updated successfully'})

# Delete a teacher by ID
@bp.route('/<int:teacher_id>', methods=['OPTIONS', 'DELETE'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher deleted successfully'})
