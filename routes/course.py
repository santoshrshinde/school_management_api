from flask import Blueprint, request, jsonify
from models import db, Course

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        'CourseID': c.CourseID,
        'CourseName': c.CourseName
    } for c in courses])

@bp.route('/', methods=['POST'])
def add_course():
    data = request.json
    course = Course(**data)
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully'}), 201