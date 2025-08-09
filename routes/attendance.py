from flask import Blueprint,request,jsonify
from extensions import db
from models import Attendance

bp=Blueprint('attendance',__name__,url_prefix='/attendance')

@bp.route('/',methods=['GET'])
def get_attendance():
    records=Attendance.query.all()
    result=[]
    for record in records:
        result.append({
            'AttendanceID': record.AttendanceID,
            'StudentID': record.StudentID,
            'Date': record.Date.strftime('%Y-%m-%d'),
            'Status': record.Status
        })
        return jsonify(result)
    
@bp.route('/', methods=['POST'])
def add_attendance():
    data = request.get_json()
    new_record = Attendance(
        StudentID=data['StudentID'],
        Date=data['Date'],
        Status=data['Status']
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message':'Attendance recorded successfully'}),201