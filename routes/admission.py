from flask import Blueprint, request, jsonify
from extensions import db
from models import Admission, Student, Course   # ✅ Student & Course bhi import karna hoga
from datetime import datetime

bp = Blueprint('admission', __name__, url_prefix='/admission')

# -------------------------
# Get all admissions (with StudentName & CourseName)
# -------------------------
@bp.route('/', methods=['GET'])
def get_admissions():
    results = db.session.query(
        Admission.AdmissionID,
        Student.Name.label("StudentName"),
        Course.CourseName.label("CourseName"),
        Admission.AdmissionDate,
        Admission.Status
    ).join(Student, Admission.StudentID == Student.StudentID
    ).join(Course, Admission.CourseID == Course.CourseID).all()

    admissions = []
    for row in results:
        admissions.append({
            "AdmissionID": row.AdmissionID,
            "StudentName": row.StudentName,
            "CourseName": row.CourseName,
            "AdmissionDate": row.AdmissionDate.strftime('%Y-%m-%d'),
            "Status": row.Status
        })

    return jsonify(admissions)

# -------------------------
# Add new admission
# -------------------------
@bp.route('/', methods=['POST'])
def add_admission():
    data = request.get_json()

    # ✅ String ko date me convert karo
    admission_date = datetime.strptime(data['AdmissionDate'], '%Y-%m-%d').date()

    new_admission = Admission(
        StudentID=data['StudentID'],
        AdmissionDate=admission_date,
        Status=data['Status'],
        CourseID=data['CourseID']
    )

    db.session.add(new_admission)
    db.session.commit()

    return jsonify({'message': 'Admission added successfully'}), 201
