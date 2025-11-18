from flask import Blueprint, request, jsonify
from extensions import db
from models import Fees, Student

bp = Blueprint('fees', __name__, url_prefix='/fees')

# ---------------- GET ALL FEES ----------------
@bp.route('/', methods=['GET'])
def get_fees():
    results = db.session.query(
        Fees.FeeID,
        Fees.Amount,
        Fees.DueDate,
        Fees.PaidAmount,
        Fees.TotalFee,
        Student.StudentID,
        Student.Name.label("StudentName")
    ).join(Student, Fees.StudentID == Student.StudentID).all()

    fees_list = []
    for row in results:
        fees_list.append({
            'FeeID': row.FeeID,
            'Amount': float(row.Amount),
            'DueDate': row.DueDate.strftime('%Y-%m-%d'),
            'PaidAmount': float(row.PaidAmount),
            'TotalFee': float(row.TotalFee),
            'StudentID': row.StudentID,   # ✅ Fix केला
            'StudentName': row.StudentName
        })
    return jsonify(fees_list)

# ---------------- GET FEE BY ID ----------------
@bp.route('/<int:id>', methods=['GET'])
def get_fee_by_id(id):
    row = db.session.query(
        Fees.FeeID,
        Fees.Amount,
        Fees.DueDate,
        Fees.PaidAmount,
        Fees.TotalFee,
        Student.StudentID,
        Student.Name.label("StudentName")
    ).join(Student, Fees.StudentID == Student.StudentID).filter(Fees.FeeID == id).first()

    if not row:
        return jsonify({"error": "Fee not found"}), 404

    return jsonify({
        'FeeID': row.FeeID,
        'Amount': float(row.Amount),
        'DueDate': row.DueDate.strftime('%Y-%m-%d'),
        'PaidAmount': float(row.PaidAmount),
        'TotalFee': float(row.TotalFee),
        'StudentID': row.StudentID,
        'StudentName': row.StudentName
    })

# ---------------- ADD NEW FEE ----------------
@bp.route('/', methods=['POST'])
def add_fee():
    data = request.get_json()
    new_fee = Fees(
        StudentID=data['StudentID'],
        Amount=data['Amount'],
        DueDate=data['DueDate'],
        PaidAmount=data['PaidAmount'],
        TotalFee=data['TotalFee']
    )
    db.session.add(new_fee)
    db.session.commit()
    return jsonify({'message': 'Fee record added successfully'}), 201

# ---------------- UPDATE FEE ----------------
@bp.route('/<int:id>', methods=['PUT'])
def update_fee(id):
    fee = Fees.query.get(id)
    if not fee:
        return jsonify({"error": "Fee not found"}), 404

    data = request.get_json()
    fee.StudentID = data.get('StudentID', fee.StudentID)
    fee.Amount = data.get('Amount', fee.Amount)
    fee.DueDate = data.get('DueDate', fee.DueDate)
    fee.PaidAmount = data.get('PaidAmount', fee.PaidAmount)
    fee.TotalFee = data.get('TotalFee', fee.TotalFee)

    db.session.commit()
    return jsonify({'message': 'Fee updated successfully'}), 200

# ---------------- DELETE FEE ----------------
@bp.route('/<int:id>', methods=['DELETE'])
def delete_fee(id):
    fee = Fees.query.get(id)
    if not fee:
        return jsonify({"error": "Fee not found"}), 404

    db.session.delete(fee)
    db.session.commit()
    return jsonify({'message': 'Fee deleted successfully'}), 200
