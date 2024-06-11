from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# initializes the app with the extension:
db.init_app(app)


# defines the Book model:
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(250), nullable=False, unique=True)
    author = db.Column(String(250), nullable=False)
    rating = db.Column(Float, nullable=False)

# alternate, more modern way to code the above block:
# class Book(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
#     author: Mapped[str] = mapped_column(String(250), nullable=False)
#     rating: Mapped[float] = mapped_column(Float, nullable=False)

# creates the database tables:
with app.app_context():
    db.create_all()

    # adds a new book entry if it doesn't exist already:
    if not Book.query.filter_by(id=1).first():
        new_book = Book(id=1, title="Harry Potter", author="J. K Rowling", rating=9.3)
        db.session.add(new_book)
        db.session.commit()
        print("New book entry added.")
    else:
        print("Book entry already exists.")

# defines a route to add a book:
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    rating = request.form['rating']
    new_book = Book(title=title, author=author, rating=rating)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('list_books'))

# Define a route to list books
@app.route('/')
def list_books():
    books = Book.query.all()
    return '<br>'.join([f'{book.title} by {book.author} (Rating: {book.rating})' for book in books]) + '<br><a href="/add_form">Add a new book</a>'

@app.route('/check_db')
def check_db():
    books = Book.query.all()
    return '<br>'.join([f'{book.id}: {book.title} by {book.author} (Rating: {book.rating})' for book in books])

@app.route('/add_form')
def add_form():
    return '''
        <form action="/add" method="post">
            <label for="title">Title</label>
            <input type="text" id="title" name="title"><br>
            <label for="author">Author</label>
            <input type="text" id="author" name="author"><br>
            <label for="rating">Rating</label>
            <input type="text" id="rating" name="rating"><br>
            <button type="submit">Add Book</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
