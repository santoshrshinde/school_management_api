from flask import Blueprint, request, jsonify
from extensions import db
from models import Attendance, Student, Course, Admission
from datetime import date

bp = Blueprint('attendance', __name__, url_prefix='/attendance')


# ============================
# ✔ GET ATTENDANCE BY COURSE + MONTH + YEAR
# ============================
@bp.route('/by-course/<int:course_id>/<int:month>/<int:year>', methods=['GET'])
def get_attendance_by_course(course_id, month, year):
    try:
        # Load students in selected course
        students = db.session.query(
            Student.StudentID,
            Student.Name
        ).join(
            Admission, Admission.StudentID == Student.StudentID
        ).filter(
            Admission.CourseID == course_id
        ).all()

        # Load DB attendance for selected month
        attendance_records = Attendance.query.filter(
            Attendance.CourseID == course_id,
            db.extract('month', Attendance.Date) == month,
            db.extract('year', Attendance.Date) == year
        ).all()

        attendance_map = {}

        # Convert DB → dictionary per student
        for record in attendance_records:
            sid = record.StudentID
            day = record.Date.day

            if sid not in attendance_map:
                attendance_map[sid] = {}

            attendance_map[sid][str(day)] = record.Status

        result = []

        # Build proper response format
        for s in students:
            sid = s.StudentID

            # Default empty attendance dict
            daily_attendance = {}

            # Fill from DB
            if sid in attendance_map:
                daily_attendance = attendance_map[sid]

            missed_days = list(daily_attendance.values()).count("A")

            result.append({
                "StudentID": sid,
                "StudentName": s.Name,
                "attendance": daily_attendance,
                "missed": missed_days
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400



# ============================
# ✔ SAVE INDIVIDUAL ATTENDANCE
# ============================
@bp.route('/', methods=['POST'])
def save_attendance():
    try:
        data = request.json

        student_id = data["StudentID"]
        course_id = data["CourseID"]
        day = data["Day"]
        month = data["Month"]
        year = data["Year"]
        status = data["Status"]

        final_date = date(year, month, day)

        record = Attendance.query.filter_by(
            StudentID=student_id,
            CourseID=course_id,
            Date=final_date
        ).first()

        if record:
            record.Status = status
        else:
            new_record = Attendance(
                StudentID=student_id,
                CourseID=course_id,
                Date=final_date,
                Status=status
            )
            db.session.add(new_record)

        db.session.commit()

        return jsonify({"message": "Attendance saved successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
