from flask import Blueprint, request, jsonify
from extensions import db
from models import Result, Student, Exam  # Correct class names

bp = Blueprint('result', __name__, url_prefix='/result')

# -------------------------
# Add new result
# -------------------------
@bp.route('/add', methods=['POST'])
def add_result():
    data = request.json
    new_result = Result(
        StudentID=data['StudentID'],
        ExamID=data['ExamID'],
        MarksObtained=data['MarksObtained'],
        Grade=data['Grade']
    )
    db.session.add(new_result)
    db.session.commit()
    return jsonify({"message": "Result added successfully"}), 201

# -------------------------
# Get all results with Student & Exam names
# -------------------------
@bp.route('/all', methods=['GET'])
def get_all_results():
    results = db.session.query(
        Result.ResultID,
        Student.Name.label("StudentName"),
        Exam.Subject.label("ExamName"),
        Result.MarksObtained,
        Result.Grade
    ).join(Student, Result.StudentID == Student.StudentID
    ).join(Exam, Result.ExamID == Exam.ExamID
    ).all()

    return jsonify([
        {
            "ResultID": r.ResultID,
            "StudentName": r.StudentName,
            "ExamName": r.ExamName,
            "MarksObtained": r.MarksObtained,
            "Grade": r.Grade
        }
        for r in results
    ])

# -------------------------
# Get result by ID with names
# -------------------------
@bp.route('/<int:result_id>', methods=['GET'])
def get_result(result_id):
    r = db.session.query(
        Result.ResultID,
        Student.Name.label("StudentName"),
        Exam.Subject.label("ExamName"),
        Result.MarksObtained,
        Result.Grade
    ).join(Student, Result.StudentID == Student.StudentID
    ).join(Exam, Result.ExamID == Exam.ExamID
    ).filter(Result.ResultID == result_id
    ).first()

    if not r:
        return jsonify({"error": "Result not found"}), 404

    return jsonify({
        "ResultID": r.ResultID,
        "StudentName": r.StudentName,
        "ExamName": r.ExamName,
        "MarksObtained": r.MarksObtained,
        "Grade": r.Grade
    })

# -------------------------
# Update result
# -------------------------
@bp.route('/update/<int:result_id>', methods=['PUT'])
def update_result(result_id):
    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    data = request.json
    result.StudentID = data.get('StudentID', result.StudentID)
    result.ExamID = data.get('ExamID', result.ExamID)
    result.MarksObtained = data.get('MarksObtained', result.MarksObtained)
    result.Grade = data.get('Grade', result.Grade)

    db.session.commit()
    return jsonify({"message": "Result updated successfully"})

# -------------------------
# Delete result
# -------------------------
@bp.route('/delete/<int:result_id>', methods=['DELETE'])
def delete_result(result_id):
    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    db.session.delete(result)
    db.session.commit()
    return jsonify({"message": "Result deleted successfully"})
