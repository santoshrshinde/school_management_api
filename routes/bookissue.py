from flask import Blueprint, request, jsonify
from extensions import db
from models import BookIssue, Student, Library  # ✅ Library used instead of Book

bp = Blueprint('bookissue', __name__, url_prefix='/bookissue')

# ✅ Get all Book Issues with Student & Library Names
@bp.route('/', methods=['GET'])
def get_all_book_issues():
    issues = db.session.query(
        BookIssue.IssueID,
        Student.Name.label('StudentName'),
        Library.BookName.label('BookName'),
        BookIssue.IssueDate,
        BookIssue.ReturnDate,
        BookIssue.Status
    ).join(Student, BookIssue.StudentID == Student.StudentID) \
     .join(Library, BookIssue.BookID == Library.BookID) \
     .all()

    result = [
        {
            'IssueID': i.IssueID,
            'StudentName': i.StudentName,
            'BookName': i.BookName,
            'IssueDate': i.IssueDate.strftime('%b %d, %Y') if i.IssueDate else None,
            'ReturnDate': i.ReturnDate.strftime('%b %d, %Y') if i.ReturnDate else None,
            'Status': i.Status  # ✅ Ensure Status is included
        } for i in issues
    ]
    return jsonify(result)


# ✅ Get single Book Issue by ID
@bp.route('/<int:id>', methods=['GET'])
def get_book_issue(id):
    issue = BookIssue.query.get_or_404(id)
    return jsonify({
        'IssueID': issue.IssueID,
        'StudentID': issue.StudentID,
        'BookID': issue.BookID,
        'IssueDate': issue.IssueDate.strftime('%Y-%m-%d') if issue.IssueDate else None,
        'ReturnDate': issue.ReturnDate.strftime('%Y-%m-%d') if issue.ReturnDate else None,
        'Status': issue.Status
    })


# ✅ Create new Book Issue
@bp.route('/', methods=['POST'])
def create_book_issue():
    data = request.json
    new_issue = BookIssue(
        StudentID=data['StudentID'],
        BookID=data['BookID'],
        IssueDate=data.get('IssueDate'),
        ReturnDate=data.get('ReturnDate'),
        Status=data.get('Status', 'Issued')
    )
    db.session.add(new_issue)
    db.session.commit()
    return jsonify({'message': 'Book issue created successfully!'}), 201


# ✅ Update Book Issue
@bp.route('/<int:id>', methods=['PUT'])
def update_book_issue(id):
    issue = BookIssue.query.get_or_404(id)
    data = request.json

    issue.StudentID = data.get('StudentID', issue.StudentID)
    issue.BookID = data.get('BookID', issue.BookID)
    issue.IssueDate = data.get('IssueDate', issue.IssueDate)
    issue.ReturnDate = data.get('ReturnDate', issue.ReturnDate)
    issue.Status = data.get('Status', issue.Status)

    db.session.commit()
    return jsonify({'message': 'Book issue updated successfully!'})


# ✅ Delete Book Issue
@bp.route('/<int:id>', methods=['DELETE'])
def delete_book_issue(id):
    issue = BookIssue.query.get_or_404(id)
    db.session.delete(issue)
    db.session.commit()
    return jsonify({'message': 'Book issue deleted successfully!'})
