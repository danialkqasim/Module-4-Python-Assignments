from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# connect to local sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# create structure for the book records
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    # just makes the output readable for me
    def __repr__(self):
        return f"{self.book_name} - {self.author}"

# simple home page
@app.route('/')
def home():
    return 'Welcome to the Library API!'

# route to get list of all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    output = []
    for book in books:
        # put every book's data into a dictionary
        data = {
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "publisher": book.publisher
        }
        output.append(data)
    return {"books": output}

# route to get a specific book using its id
@app.route('/books/<id>', methods=['GET'])
def get_single_book(id):
    book = Book.query.get_or_404(id)
    return {
        "book_name": book.book_name, 
        "author": book.author, 
        "publisher": book.publisher
    }

# route to add new book to the database
@app.route('/books', methods=['POST'])
def add_new_book():
    new_book = Book(
        book_name=request.json['book_name'],
        author=request.json['author'],
        publisher=request.json['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    # return the id so I know it was created
    return {'id': new_book.id}

# route to delete book by id
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "that book doesn't exist"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "book has been deleted"}

if __name__ == '__main__':
    # makes sure the database is created when the script starts
    with app.app_context():
        db.create_all()
    app.run(debug=True)