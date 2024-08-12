import sqlite3
import hashlib
import json
import datetime
import os
from flask import g, current_app, session
import mistune

DATABASE = 'User.db'
POSTS_DATABASE_DIR = 'static/POSTS'

def get_db(db_name=DATABASE):
    if 'db' not in g:
        g.db = sqlite3.connect(db_name)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

class User:
    def __init__(self):
        pass

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, email, age, phone_number):
        try:
            db = get_db()
            cursor = db.cursor()
            hashed_password = self.hash_password(password)
            hashed_username = self.hash_password(username)
            
            cursor.execute("INSERT INTO pending_users (username, hashed_username, password, email, age, phone_number) VALUES (?, ?, ?, ?, ?, ?)",
                            (username, hashed_username, hashed_password, email, age, phone_number))
            db.commit()
            return json.dumps({"status": 200, "msg": "Registration request submitted successfully"})
        except sqlite3.IntegrityError:
            return json.dumps({"status": 400, "msg": "Username already exists"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def login(self, username, password):
        try:
            db = get_db()
            cursor = db.cursor()
            hashed_password = self.hash_password(password)
            cursor.execute("SELECT * FROM users WHERE hashed_username = ? AND password = ?", (self.hash_password(username), hashed_password))
            if cursor.fetchone():
                return json.dumps({"status": 200, "msg": "Login successful"})
            return json.dumps({"status": 400, "msg": "Invalid username or password"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def logout(self, username):
        return json.dumps({"status": 200, "msg": "Logout successful"})

    def create_table(self, username):
        try:
            db = get_db()
            cursor = db.cursor()
            safe_username = f"user_{username}"
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {safe_username} (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)
            """)
            db.commit()
            return json.dumps({"status": 200, "msg": f"Table for {username} created successfully"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def store_post_id(self, username, post_id):
        try:
            db = get_db()
            cursor = db.cursor()
            safe_username = f"user_{username}"
            cursor.execute(f"INSERT INTO {safe_username} (post_id) VALUES (?)", (post_id,))
            db.commit()
            return json.dumps({"status": 200, "msg": "Post ID stored successfully"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

class POSTS:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect_to_db(self):
        current_month = datetime.datetime.now().strftime("%Y_%m")
        db_name = os.path.join(POSTS_DATABASE_DIR, f'Post_{current_month}.db')
        self.db = sqlite3.connect(db_name)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_title TEXT NOT NULL,
                post_content TEXT NOT NULL,
                post_author TEXT NOT NULL,
                tags TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)
            """)
            self.db.commit()
        except sqlite3.Error as e:
            self.log_activity("Error initializing POSTS class: " + str(e))

    def create_post(self, post_title, post_content, post_author, tags):
        self.connect_to_db()
        try:
            markdown = mistune.create_markdown()
            html_content = markdown(post_content)

            self.cursor.execute("INSERT INTO posts (post_title, post_content, post_author, tags) VALUES (?, ?, ?, ?)", 
                                (post_title, html_content, post_author, tags))
            self.db.commit()
            return json.dumps({"status": 200, "msg": "Post created successfully"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def delete_post(self, post_id):
        self.connect_to_db()
        try:
            self.cursor.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
            self.db.commit()
            return json.dumps({"status": 200, "msg": "Post deleted successfully"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def get_posts(self):
        self.connect_to_db()
        try:
            self.cursor.execute("SELECT * FROM posts ORDER BY timestamp DESC")
            posts = self.cursor.fetchall()
            return json.dumps({"status": 200, "msg": "Posts fetched successfully", "data": [dict(post) for post in posts]})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def get_post_by_id(self, post_id):
        self.connect_to_db()
        try:
            self.cursor.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
            post = self.cursor.fetchone()
            if post:
                return json.dumps({"status": 200, "msg": "Post fetched successfully", "data": dict(post)})
            else:
                return json.dumps({"status": 404, "msg": "Post not found"})
        except sqlite3.Error as e:
            return json.dumps({"status": 500, "msg": "Internal server error"})

    def log_activity(self, message):
        log_file = 'log.txt'
        with open(log_file, 'a') as f:
            log_message = f"{datetime.datetime.now()} - {message}\n"
            f.write(log_message)

class Admin:
    def __init__(self, app=None):
        if app:
            with app.app_context():
                self.ensure_admin_table()

    def log_activity(self, admin_username, action, status):
        log_file = 'admin_log.txt'
        with open(log_file, 'a') as f:
            log_message = f"{datetime.datetime.now()} - Admin: {admin_username} - Action: {action} - Status: {status}\n"
            f.write(log_message)

    def ensure_admin_table(self):
        db = get_db('User.db')
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                hashed_username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone_number TEXT NOT NULL)
            """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS pending_users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                hashed_username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone_number TEXT NOT NULL)
            """)
        db.commit()
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        if cursor.fetchone()[0] == 0:
            self.create_default_admin()

    def create_default_admin(self):
        default_username = 'admin'
        default_password = 'admin_password'  # Replace with a secure default password
        hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
        db = get_db('User.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO admin_users (username, password) VALUES (?, ?)",
                       (default_username, hashed_password))
        db.commit()

    def authenticate(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db = get_db('User.db')
        cur = db.execute('SELECT * FROM admin_users WHERE username = ? AND password = ?', (username, hashed_password))
        return cur.fetchone()

    def get_registered_users(self):
        db = get_db('User.db')
        cursor = db.execute('SELECT * FROM users')
        return cursor.fetchall()

    def get_pending_users(self):
        db = get_db('User.db')
        cursor = db.execute('SELECT * FROM pending_users')
        return cursor.fetchall()

    def approve_user(self, user_id):
        db = get_db('User.db')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM pending_users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            cursor.execute('SELECT * FROM users WHERE username = ? OR email = ? OR phone_number = ?', 
                            (user['username'], user['email'], user['phone_number']))
            if cursor.fetchone():
                self.log_activity(session.get('admin'), f'Approve User ID {user_id}', 'Failed - User already exists')
                return json.dumps({"status": 400, "msg": "User already exists in the system"})
            
            cursor.execute('INSERT INTO users (username, hashed_username, password, email, age, phone_number) VALUES (?, ?, ?, ?, ?, ?)', 
                            (user['username'], user['hashed_username'], user['password'], user['email'], user['age'], user['phone_number']))
            cursor.execute('DELETE FROM pending_users WHERE user_id = ?', (user_id,))
            db.commit()
            self.log_activity(session.get('admin'), f'Approve User ID {user_id}', 'Success')
            return json.dumps({"status": 200, "msg": "User approved successfully"})
        self.log_activity(session.get('admin'), f'Approve User ID {user_id}', 'Failed - User not found')
        return json.dumps({"status": 404, "msg": "User not found"})

    def deny_user(self, user_id):
        db = get_db('User.db')
        cursor = db.cursor()
        cursor.execute('DELETE FROM pending_users WHERE user_id = ?', (user_id,))
        db.commit()
        self.log_activity(session.get('admin'), f'Deny User ID {user_id}', 'Success')

    def delete_user(self, user_id):
        db = get_db('User.db')
        cursor = db.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        db.commit()
        self.log_activity(session.get('admin'), f'Delete User ID {user_id}', 'Success')

    def reset_password(self, username, new_password):
        try:
            db = get_db()
            cursor = db.cursor()
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
            db.commit()
            self.log_activity(username, 'Reset Password', 'Success')
            return json.dumps({"status": 200, "msg": "Password reset successfully"})
        except sqlite3.Error as e:
            self.log_activity(username, 'Reset Password', 'Failed - ' + str(e))
            return json.dumps({"status": 500, "msg": "Internal server error"})
