from flask import Blueprint, request, jsonify
from extensions import db
from models import Exam

bp = Blueprint('exam', __name__, url_prefix='/exam')

# Add a new exam
@bp.route('/add', methods=['POST'])
def add_exam():
    data = request.get_json()
    new_exam = Exam(
        CourseID=data['CourseID'],
        Subject=data['Subject'],
        ExamDate=data['ExamDate'],
        TotalMarks=data['TotalMarks']
    )
    db.session.add(new_exam)
    db.session.commit()
    return jsonify({"message": "Exam added successfully!"}), 201

# Get all exams
@bp.route('/all', methods=['GET'])
def get_exams():
    exams = Exam.query.all()
    result = []
    for e in exams:
        result.append({
            "ExamID": e.ExamID,
            "CourseID": e.CourseID,
            "Subject": e.Subject,
            "ExamDate": e.ExamDate.strftime('%Y-%m-%d'),
            "TotalMarks": e.TotalMarks
        })
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def get_exam(id):
    exam = Exam.query.get(id)
    if exam:
        return jsonify({
            "ExamID": exam.ExamID,
            "CourseID": exam.CourseID,
            "Subject": exam.Subject,
            "ExamDate": exam.ExamDate.strftime('%Y-%m-%d'),
            "TotalMarks": exam.TotalMarks
        })
    return jsonify({"error": " Exam not found"}), 404

@bp.route('/update/<int:id>', methods=['PUT'])
def update_exam(id):
    exam = Exam.query.get(id)
    if not exam:
        return jsonify({"error": " Exam not found"}), 404

    data = request.get_json()
    exam.CourseID = data.get('CourseID', exam.CourseID)
    exam.Subject = data.get('Subject', exam.Subject)
    exam.ExamDate = data.get('ExamDate', exam.ExamDate)
    exam.TotalMarks = data.get('TotalMarks', exam.TotalMarks)

    db.session.commit()
    return jsonify({"message": " Exam updated successfully!"})

# Delete exam
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_exam(id):
    exam = Exam.query.get(id)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    db.session.delete(exam)
    db.session.commit()
    return jsonify({"message": " Exam deleted successfully!"})
