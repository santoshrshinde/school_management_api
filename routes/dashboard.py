from flask import Blueprint, jsonify
from extensions import db
from sqlalchemy import text

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/count', methods=['GET'])
def dashboard_count():

    total_students = db.session.execute(
        text("SELECT COUNT(*) FROM Stds")
    ).scalar()

    total_teachers = db.session.execute(
        text("SELECT COUNT(*) FROM Teacher")
    ).scalar()

    total_courses = db.session.execute(
        text("SELECT COUNT(*) FROM Course")
    ).scalar()

    total_admissions = db.session.execute(
        text("SELECT COUNT(*) FROM Admission")
    ).scalar()

    return jsonify({
        "totalStudents": int(total_students),
        "totalTeachers": int(total_teachers),
        "totalCourses": int(total_courses),
        "totalAdmissions": int(total_admissions)
    })
