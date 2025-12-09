from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import requests
from functools import wraps
import logging

app = Flask(__name__)
app.secret_key = 'my-secret-key-shall cgange-in-production'

# Optional: basic logging to help debug session issues
logging.basicConfig(level=logging.DEBUG)

DATABASE = 'books.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database"""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    """Main page showing user's books"""
    db = get_db()
    books = db.execute(
        'SELECT * FROM books WHERE user_id = ? ORDER BY id DESC',
        (session['user_id'],)
    ).fetchall()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    # If already logged in, send to index to avoid showing the login form again
    if 'user_id' in session:
        app.logger.debug(f"User already in session: {dict(session)}")
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            # ensure session is marked as modified (helps in some setups)
            session.modified = True
            app.logger.debug(f"Session after login (POST): {dict(session)}")
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            app.logger.debug(f"Failed login attempt for username: {username}")
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
@login_required
def search_book():
    """Search for a book by ISBN using Google Books API"""
    isbn = request.form.get('isbn', '').strip()
    
    if not isbn:
        flash('Please enter an ISBN.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Call Google Books API
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'items' not in data or len(data['items']) == 0:
            flash(f'No book found with ISBN: {isbn}', 'error')
            return redirect(url_for('index'))
        
        # Get first result
        book_info = data['items'][0]['volumeInfo']
        
        # Extract book details
        title = book_info.get('title', 'Unknown Title')
        authors = ', '.join(book_info.get('authors', ['Unknown Author']))
        page_count = book_info.get('pageCount', 0)
        average_rating = book_info.get('averageRating', 0.0)
        
        # Get thumbnail URL (extra credit)
        thumbnail = None
        if 'imageLinks' in book_info:
            thumbnail = book_info['imageLinks'].get('thumbnail')
