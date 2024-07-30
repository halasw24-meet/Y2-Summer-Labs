from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    wishlist = db.relationship('Book', secondary='wishlist', backref='users_wishlist')
    reading_list = db.relationship('Book', secondary='reading_list', backref='users_reading')
    finished_list = db.relationship('Book', secondary='finished_list', backref='users_finished')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    cover_url = db.Column(db.String(250), nullable=False)

wishlist = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

reading_list = db.Table('reading_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

finished_list = db.Table('finished_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    books = Book.query.limit(9).all()
    return render_template('home.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        action = request.form['action']
        if action == 'wishlist':
            current_user.wishlist.append(book)
        elif action == 'reading':
            current_user.reading_list.append(book)
        elif action == 'finished':
            current_user.finished_list.append(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('book.html', book=book)

@app.route('/lists')
@login_required
def lists():
    return render_template('lists.html')

if __name__ == '__main__':
    app.run(debug=True)