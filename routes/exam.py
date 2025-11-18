from flask import Blueprint, request, jsonify
from extensions import db
from models import Exam, Course
from datetime import datetime
from flask_cors import CORS

bp = Blueprint('exam', __name__, url_prefix='/exam')
CORS(bp, resources={r"/*": {"origins": "*"}})  # Allow all origins

# ------------------ Add new exam -------------------
@bp.route('/add', methods=['POST'])
def add_exam():
    data = request.get_json()

    if not data.get('CourseID'):
        return jsonify({"error": "CourseID is required"}), 400

    try:
        new_exam = Exam(
            CourseID=data['CourseID'],
            Subject=data['Subject'],
            ExamDate=datetime.strptime(data['ExamDate'], '%Y-%m-%d').date(),
            TotalMarks=data['TotalMarks']
        )
        db.session.add(new_exam)
        db.session.commit()
        return jsonify({"message": "Exam added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ------------------ Get all exams -------------------
@bp.route('/all', methods=['GET'])
def get_exams():
    exams = db.session.query(
        Exam.ExamID,
        Course.CourseName.label("CourseName"),
        Exam.Subject,
        Exam.ExamDate,
        Exam.TotalMarks
    ).join(Course, Exam.CourseID == Course.CourseID).all()

    result = [
        {
            "ExamID": e.ExamID,
            "CourseName": e.CourseName,
            "Subject": e.Subject,
            "ExamDate": e.ExamDate.strftime('%Y-%m-%d'),
            "TotalMarks": e.TotalMarks
        } for e in exams
    ]
    return jsonify(result)


# ------------------ Get single exam -------------------
@bp.route('/<int:id>', methods=['GET'])
def get_exam(id):
    exam = db.session.query(
        Exam.ExamID,
        Exam.CourseID,
        Course.CourseName.label("CourseName"),
        Exam.Subject,
        Exam.ExamDate,
        Exam.TotalMarks
    ).join(Course, Exam.CourseID == Course.CourseID).filter(Exam.ExamID == id).first()

    if exam: 
        return jsonify({
            "ExamID": exam.ExamID,
            "CourseID": exam.CourseID,
            "CourseName": exam.CourseName,
            "Subject": exam.Subject,
            "ExamDate": exam.ExamDate.strftime('%Y-%m-%d'),
            "TotalMarks": exam.TotalMarks
        })
    return jsonify({"error": "Exam not found"}), 404


# ------------------ Update exam -------------------
@bp.route('/update/<int:id>', methods=['PUT'])
def update_exam(id):
    exam = Exam.query.get(id)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    data = request.get_json()
    exam.CourseID = data.get('CourseID', exam.CourseID)
    exam.Subject = data.get('Subject', exam.Subject)
    if 'ExamDate' in data:
        exam.ExamDate = datetime.strptime(data['ExamDate'], '%Y-%m-%d').date()
    exam.TotalMarks = data.get('TotalMarks', exam.TotalMarks)

    db.session.commit()
    return jsonify({"message": "Exam updated successfully!"})


# ------------------ Delete exam -------------------
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_exam(id):
    exam = Exam.query.get(id)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    db.session.delete(exam)
    db.session.commit()
    return jsonify({"message": "Exam deleted successfully!"})


# ------------------ Get courses for dropdown -------------------
@bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    result = [{"CourseID": c.CourseID, "CourseName": c.CourseName} for c in courses]
    return jsonify(result)
