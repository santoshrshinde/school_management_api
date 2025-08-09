from flask import Blueprint,request,jsonify
from extensions import db 
from models import Fees

bp=Blueprint('fees',__name__,url_prefix='/fees')

@bp.route('/',methods=['GET'])
def get_fees():
    records=Fees.query.all()
    result=[]
    for fee in records:
        result=[]
        for fee in records:
            result.append({
                'FeeID':fee.FeeID,
                'StudentID':fee.StudentID,
                'Amount': float(fee.Amount),
                'DueDate': fee.DueDate.strftime('%Y-%m-%d'),
                'PaidAmount': float(fee.PaidAmount),
                'TotalFee': float(fee.TotalFee)
            })
    return jsonify(result)
@bp.route('/',methods=['POST'])
def add_fee():
    data=request.get_json()
    new_fee=Fees(
        StudentID=data['StudentID'],
        Amount=data['Amount'],
        DueDate=data['DueDate'],
        PaidAmount=data['PaidAmount'],
        TotalFee=data['TotalFee']
    )
    db.session.add(new_fee)
    db.session.commit()
    return jsonify({'message':'Fee record added successfully'}),201
