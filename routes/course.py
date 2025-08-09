from flask import Blueprint, jsonify, request
from models import Course
from extensions import db

bp = Blueprint('course', __name__, url_prefix='/courses')

# Get all courses
@bp.route('/', methods=['OPTIONS', 'GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {
            'CourseID': course.CourseID,
            'CourseName': course.CourseName
        }
        for course in courses
    ])

# Add a new course
@bp.route('/', methods=['OPTIONS', 'POST'])
def add_course():
    data = request.get_json()
    course = Course(**data)
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully'}), 201

# Get a single course by ID
@bp.route('/<int:course_id>', methods=['OPTIONS', 'GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        'CourseID': course.CourseID,
        'CourseName': course.CourseName
    })

# Update a course by ID
@bp.route('/<int:course_id>', methods=['OPTIONS', 'PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    course.CourseName = data['CourseName']
    db.session.commit()
    return jsonify({'message': 'Course updated successfully'})

# Delete a course by ID
@bp.route('/<int:course_id>', methods=['OPTIONS', 'DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})
