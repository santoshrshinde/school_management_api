from flask import Blueprint, request, jsonify
from models import db, Teacher

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
    data = request.json
    teacher = Teacher(**data)
    db.session.add(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher added successfully'}), 201