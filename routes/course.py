from flask import Blueprint, jsonify
from models import Course
from extensions import db

bp = Blueprint('course', __name__, url_prefix='/courses')

@bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {
            'CourseID': course.CourseID,
            'CourseName': course.CourseName
        }
        for course in courses
    ])
