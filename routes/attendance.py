from flask import Blueprint, request, jsonify
from extensions import db
from models import Attendance, Student
from dateutil.parser import parse  # ✅ handles ISO date strings

bp = Blueprint('attendance', __name__, url_prefix='/attendance')


# Get all attendance records with student names
@bp.route('/', methods=['GET'])
def get_all_attendance():
    records = db.session.query(
        Attendance.AttendanceID,
        Student.Name.label("StudentName"),
        Attendance.Date,
        Attendance.Status
    ).join(Student, Attendance.StudentID == Student.StudentID).all()

    result = [
        {
            "AttendanceID": r.AttendanceID,
            "StudentName": r.StudentName,
            "Date": r.Date.strftime('%Y-%m-%d') if r.Date else None,
            "Status": r.Status
        } for r in records
    ]
    return jsonify(result)


# Get single attendance record by ID
@bp.route('/<int:id>', methods=['GET'])
def get_attendance(id):
    record = Attendance.query.get_or_404(id)
    student = Student.query.get(record.StudentID)
    return jsonify({
        "AttendanceID": record.AttendanceID,
        "StudentID": record.StudentID,
        "StudentName": student.Name if student else None,
        "Date": record.Date.strftime('%Y-%m-%d') if record.Date else None,
        "Status": record.Status
    })


# Create new attendance record
@bp.route('/', methods=['POST'])
def create_attendance():
    data = request.json
    try:
        # Convert ISO datetime or YYYY-MM-DD string to date
        date_obj = parse(data['Date']).date() if data.get('Date') else None

        new_attendance = Attendance(
            StudentID=data['StudentID'],
            Date=date_obj,
            Status=data.get('Status', 'Present')
        )
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'message': 'Attendance added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Update attendance record
@bp.route('/<int:id>', methods=['PUT'])
def update_attendance(id):
    record = Attendance.query.get_or_404(id)
    data = request.json

    record.StudentID = data.get('StudentID', record.StudentID)
    if data.get('Date'):
        record.Date = parse(data['Date']).date()
    record.Status = data.get('Status', record.Status)

    db.session.commit()
    return jsonify({'message': 'Attendance updated successfully!'})


# Delete attendance record
@bp.route('/<int:id>', methods=['DELETE'])
def delete_attendance(id):
    record = Attendance.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Attendance deleted successfully!'})
