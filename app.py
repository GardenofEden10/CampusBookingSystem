from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secret random string

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# User class for Flask-Login
class User(UserMixin):

    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


# Load user from database
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE UserID = ?", (user_id, ))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[4])
    return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username = ?", (username, ))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[3], password):
            login_user(User(user[0], user[1], user[4]))
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
