from flask import Blueprint, jsonify, request
from extensions import db
from models import Timetable, Course, Teacher

# Blueprint setup
bp = Blueprint('timetable', __name__, url_prefix='/timetable')

# ---------------------------------------------------
# 📘 1️⃣ Get all timetables (with CourseName & TeacherName)
# ---------------------------------------------------
@bp.route('/all', methods=['GET'])
def get_all_timetables():
    timetables = (
        db.session.query(
            Timetable.TimetableID,
            Course.CourseName,
            Timetable.Day,
            Timetable.TimeSlot,
            Timetable.Subject,
            Teacher.Name.label("TeacherName")
        )
        .join(Course, Timetable.CourseID == Course.CourseID)
        .join(Teacher, Timetable.TeacherID == Teacher.TeacherID)
        .all()
    )

    result = [
        {
            "TimetableID": t.TimetableID,
            "CourseName": t.CourseName,
            "Day": t.Day,
            "TimeSlot": t.TimeSlot,
            "Subject": t.Subject,
            "TeacherName": t.TeacherName
        }
        for t in timetables
    ]
    return jsonify(result)

# ---------------------------------------------------
# 📘 2️⃣ Add new timetable record
# ---------------------------------------------------
@bp.route('/add', methods=['POST'])
def add_timetable():
    data = request.get_json()

    try:
        new_timetable = Timetable(
            CourseID=data.get('CourseID'),
            TeacherID=data.get('TeacherID'),
            Day=data.get('Day'),
            TimeSlot=data.get('TimeSlot'),
            Subject=data.get('Subject')
        )
        db.session.add(new_timetable)
        db.session.commit()
        return jsonify({"message": "Timetable added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# ---------------------------------------------------
# 📘 3️⃣ Get timetable by ID (for editing)
# ---------------------------------------------------
@bp.route('/<int:id>', methods=['GET'])
def get_timetable(id):
    timetable = Timetable.query.get_or_404(id)
    course = Course.query.get(timetable.CourseID)
    teacher = Teacher.query.get(timetable.TeacherID)

    result = {
        "TimetableID": timetable.TimetableID,
        "CourseID": timetable.CourseID,
        "CourseName": course.CourseName if course else None,
        "TeacherID": timetable.TeacherID,
        "TeacherName": teacher.Name if teacher else None,
        "Day": timetable.Day,
        "TimeSlot": timetable.TimeSlot,
        "Subject": timetable.Subject
    }
    return jsonify(result)

# ---------------------------------------------------
# 📘 4️⃣ Update timetable by ID
# ---------------------------------------------------
@bp.route('/update/<int:id>', methods=['PUT'])
def update_timetable(id):
    data = request.get_json()
    timetable = Timetable.query.get_or_404(id)

    try:
        timetable.CourseID = data.get('CourseID')
        timetable.TeacherID = data.get('TeacherID')
        timetable.Day = data.get('Day')
        timetable.TimeSlot = data.get('TimeSlot')
        timetable.Subject = data.get('Subject')

        db.session.commit()
        return jsonify({"message": "Timetable updated successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# ---------------------------------------------------
# 📘 5️⃣ Delete timetable by ID
# ---------------------------------------------------
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_timetable(id):
    timetable = Timetable.query.get_or_404(id)

    try:
        db.session.delete(timetable)
        db.session.commit()
        return jsonify({"message": "Timetable deleted successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
