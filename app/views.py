import os
from flask import Blueprint, jsonify, request
from .models import Book, db
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'

# Убедитесь, что папка существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello Python!"}), 200

@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "grade": book.grade,
            "subject": book.subject,
            "download_url": book.download_url
        }
        for book in books
    ]
    return jsonify(result), 200

@bp.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    grade = request.form.get('grade')
    subject = request.form.get('subject')

    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        download_url = file_path
    else:
        return jsonify({"message": "No file provided"}), 400

    new_book = Book(
        title=title,
        author=author,
        grade=grade,
        subject=subject,
        download_url=download_url
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 201