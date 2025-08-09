from flask import Blueprint, jsonify, request
from models import Library
from extensions import db

bp = Blueprint('library', __name__, url_prefix='/library')

# Get all books
@bp.route('/', methods=['OPTIONS', 'GET'])
def get_books():
    books = Library.query.all()
    return jsonify([
        {
            'BookID': book.BookID,
            'BookName': book.BookName,
            'Author': book.Author,
            'Publisher': book.Publisher,
            'TotalQuantity': book.TotalQuantity,
            'AvailableQuantity': book.AvailableQuantity
        }
        for book in books
    ])

# Add a new book
@bp.route('/', methods=['OPTIONS', 'POST'])
def add_book():
    data = request.get_json()
    new_book = Library(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

# Get single book
@bp.route('/<int:book_id>', methods=['OPTIONS', 'GET'])
def get_book(book_id):
    book = Library.query.get_or_404(book_id)
    return jsonify({
        'BookID': book.BookID,
        'BookName': book.BookName,
        'Author': book.Author,
        'Publisher': book.Publisher,
        'TotalQuantity': book.TotalQuantity,
        'AvailableQuantity': book.AvailableQuantity
    })

# Update book
@bp.route('/<int:book_id>', methods=['OPTIONS', 'PUT'])
def update_book(book_id):
    book = Library.query.get_or_404(book_id)
    data = request.get_json()
    book.BookName = data['BookName']
    book.Author = data['Author']
    book.Publisher = data['Publisher']
    book.TotalQuantity = data['TotalQuantity']
    book.AvailableQuantity = data['AvailableQuantity']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

# Delete book
@bp.route('/<int:book_id>', methods=['OPTIONS', 'DELETE'])
def delete_book(book_id):
    book = Library.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})
