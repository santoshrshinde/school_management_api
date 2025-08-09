from flask import Blueprint, request, jsonify
from extensions import db
from models import Timetable

bp = Blueprint('timetable', __name__, url_prefix='/timetable')


@bp.route('/add', methods=['POST'])
def add_timetable():
    data = request.get_json()
    new_entry = Timetable(
        CourseID=data['CourseID'],
        Day=data['Day'],
        TimeSlot=data['TimeSlot'],
        Subject=data['Subject'],
        TeacherID=data['TeacherID']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": " Timetable entry added successfully"})

@bp.route('/all', methods=['GET'])
def get_all_timetables():
    timetables = Timetable.query.all()
    return jsonify([
        {
            "TimetableID": t.TimetableID,
            "CourseID": t.CourseID,
            "Day": t.Day,
            "TimeSlot": t.TimeSlot,
            "Subject": t.Subject,
            "TeacherID": t.TeacherID
        }
        for t in timetables
    ])

@bp.route('/<int:id>', methods=['GET'])
def get_timetable(id):
    t = Timetable.query.get(id)
    if not t:
        return jsonify({"error": " Timetable entry not found"}), 404
    return jsonify({
        "TimetableID": t.TimetableID,
        "CourseID": t.CourseID,
        "Day": t.Day,
        "TimeSlot": t.TimeSlot,
        "Subject": t.Subject,
        "TeacherID": t.TeacherID
    })

@bp.route('/update/<int:id>', methods=['PUT'])
def update_timetable(id):
    t = Timetable.query.get(id)
    if not t:
        return jsonify({"error": " Timetable entry not found"}), 404
    
    data = request.get_json()
    t.CourseID = data.get('CourseID', t.CourseID)
    t.Day = data.get('Day', t.Day)
    t.TimeSlot = data.get('TimeSlot', t.TimeSlot)
    t.Subject = data.get('Subject', t.Subject)
    t.TeacherID = data.get('TeacherID', t.TeacherID)
    db.session.commit()
    return jsonify({"message": " Timetable updated successfully"})

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_timetable(id):
    t = Timetable.query.get(id)
    if not t:
        return jsonify({"error": " Timetable entry not found"}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": " Timetable deleted successfully"})
