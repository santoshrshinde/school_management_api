from flask import Blueprint, jsonify, request
from models import Teacher
from extensions import db

bp = Blueprint('teacher', __name__, url_prefix='/teachers')

@bp.route('/', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([{
        'TeacherID': t.TeacherID,
        'Name': t.Name,
        'Subject': t.Subject,
        'Contact': t.Contact
    } for t in teachers])

@bp.route('/', methods=['POST'])
def add_teacher():
    data = request.get_json()
    new_teacher = Teacher(
        Name=data['Name'],
        Subject=data['Subject'],
        Contact=data['Contact']
    )
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher added successfully'})
