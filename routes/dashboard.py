from flask import Blueprint, jsonify
from extensions import db
from datetime import date
from sqlalchemy import text

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/summary', methods=['GET'])
def dashboard_summary():
    try:
        total_students = db.session.execute(
            text("SELECT COUNT(*) FROM students")
        ).scalar()

        total_teachers = db.session.execute(
            text("SELECT COUNT(*) FROM teacher")
        ).scalar()

        total_courses = db.session.execute(
            text("SELECT COUNT(*) FROM course")
        ).scalar()

        # ✅ Pending Fees Calculation
        pending_fees = db.session.execute(
            text("SELECT IFNULL(SUM(total_fees - paid_amount), 0) FROM fees")
        ).scalar()

        today = date.today()

        total_attendance = db.session.execute(
            text("SELECT COUNT(*) FROM attendance WHERE date = :d"),
            {"d": today}
        ).scalar()

        present_attendance = db.session.execute(
            text(
                "SELECT COUNT(*) FROM attendance "
                "WHERE date = :d AND status = 'Present'"
            ),
            {"d": today}
        ).scalar()

        attendance_percent = 0
        if total_attendance > 0:
            attendance_percent = round(
                (present_attendance / total_attendance) * 100, 2
            )

        return jsonify({
            "totalStudents": total_students,
            "totalTeachers": total_teachers,
            "totalCourses": total_courses,
            "pendingFees": pending_fees,
            "attendancePercent": attendance_percent
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
