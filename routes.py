from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Example decorator to check if user is logged in
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'credentials' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))  # Redirect to login page if not logged in
        return func(*args, **kwargs)  # Call the original function if logged in
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
@login_required
def about():
    return "Welcome to the about page"

@app.route('/contact')
@login_required
def contact():
    return "Welcome to the contact page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['credentials'] = request.form['username']
        flash('You were successfully logged in', 'success')
        return redirect(url_for('dashboard'))  # Redirect to dashboard after login

    return render_template('login_registration.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        # Handle form submission to create a new post
        # Example: Save post data to database, etc.
        flash('Post created successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_post.html')

@app.route('/register', methods=['POST'])
def register():
    # Handle form submission to register a new user
    # Example: Save user data to database, etc.
    flash('You were successfully registered', 'success')
    return redirect(url_for('login'))