from flask import Blueprint, request, jsonify
from extensions import db
from models import Admission

bp = Blueprint('admission', __name__, url_prefix='/admission')

@bp.route('/', methods=['GET'])
def get_admissions():
    admissions = Admission.query.all()
    result = []
    for admission in admissions:
        result.append({
            'AdmissionID': admission.AdmissionID,
            'StudentID': admission.StudentID,
            'AdmissionDate': admission.AdmissionDate.strftime('%Y-%m-%d'),
            'Status': admission.Status,
            'CourseID': admission.CourseID
        })
    return jsonify(result)

@bp.route('/', methods=['POST'])
def add_admission():
    data = request.get_json()
    new_admission = Admission(
        StudentID=data['StudentID'],
        AdmissionDate=data['AdmissionDate'],
        Status=data['Status'],
        CourseID=data['CourseID']
    )
    db.session.add(new_admission)
    db.session.commit()
    return jsonify({'message': 'Admission added successfully'}), 201
