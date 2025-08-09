from flask import Blueprint, request, jsonify
from extensions import db
from models import Result

bp = Blueprint('result', __name__, url_prefix='/result')

# -------------------------
# Add new result (POST method for actual use)
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
# Temporary: Add result using GET (for quick browser testing)
# -------------------------
@bp.route('/add-test', methods=['GET'])
def add_result_test():
    new_result = Result(
        StudentID=1,
        ExamID=1,
        MarksObtained=90,
        Grade="A+"
    )
    db.session.add(new_result)
    db.session.commit()
    return jsonify({"message": "Sample result added successfully (GET method)"}), 201

# -------------------------
# Get all results
# -------------------------
@bp.route('/all', methods=['GET'])
def get_all_results():
    results = Result.query.all()
    return jsonify([
        {
            "ResultID": r.ResultID,
            "StudentID": r.StudentID,
            "ExamID": r.ExamID,
            "MarksObtained": r.MarksObtained,
            "Grade": r.Grade
        }
        for r in results
    ])

# -------------------------
# Get result by ID
# -------------------------
@bp.route('/<int:result_id>', methods=['GET'])
def get_result(result_id):
    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404
    return jsonify({
        "ResultID": result.ResultID,
        "StudentID": result.StudentID,
        "ExamID": result.ExamID,
        "MarksObtained": result.MarksObtained,
        "Grade": result.Grade
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
