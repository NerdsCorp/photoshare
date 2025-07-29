from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import os
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database setup
def init_db():
    with sqlite3.connect('admins.db') as conn:
        c = conn.cursor()
        # Admin table
        c.execute('''CREATE TABLE IF NOT EXISTS admins
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL)''')
        # Add default admin if table is empty
        c.execute("SELECT COUNT(*) FROM admins")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
                      ('admin', generate_password_hash('gallery123', method='pbkdf2:sha256')))
        # Image descriptions table
        c.execute('''CREATE TABLE IF NOT EXISTS image_descriptions
                     (filename TEXT PRIMARY KEY,
                      description TEXT NOT NULL)''')
        conn.commit()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    images = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    descriptions = {}
    with sqlite3.connect('admins.db') as conn:
        c = conn.cursor()
        for image in images:
            c.execute("SELECT description FROM image_descriptions WHERE filename = ?", (image,))
            result = c.fetchone()
            descriptions[image] = result[0] if result else ""
    return render_template('index.html', images=images, descriptions=descriptions, logged_in=session.get('logged_in', False))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('admins.db') as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM admins WHERE username = ?", (username,))
            result = c.fetchone()
            if result and check_password_hash(result[0], password):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('admin'))
            else:
                flash('Invalid credentials. Please try again.')
                return redirect(url_for('index'))
    return render_template('index.html', login=True)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Images uploaded successfully!')
        return redirect(url_for('admin'))
    
    images = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    descriptions = {}
    with sqlite3.connect('admins.db') as conn:
        c = conn.cursor()
        for image in images:
            c.execute("SELECT description FROM image_descriptions WHERE filename = ?", (image,))
            result = c.fetchone()
            descriptions[image] = result[0] if result else ""
    return render_template('index.html', images=images, descriptions=descriptions, logged_in=True)

@app.route('/manage_admins', methods=['GET', 'POST'])
def manage_admins():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    with sqlite3.connect('admins.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            if 'add_admin' in request.form:
                username = request.form['new_username']
                password = request.form['new_password']
                try:
                    c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
                              (username, generate_password_hash(password, method='pbkdf2:sha256')))
                    conn.commit()
                    flash('Admin added successfully!')
                except sqlite3.IntegrityError:
                    flash('Username already exists.')
            elif 'delete_admin' in request.form:
                username = request.form['username']
                if username != session.get('username'):  # Prevent self-deletion
                    c.execute("DELETE FROM admins WHERE username = ?", (username,))
                    conn.commit()
                    flash('Admin deleted successfully!')
                else:
                    flash('You cannot delete your own account.')
        
        c.execute("SELECT username FROM admins")
        admins = [row[0] for row in c.fetchall()]
    
    return render_template('index.html', images=None, descriptions=None, logged_in=True, manage_admins=True, admins=admins)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path) and allowed_file(filename):
        os.unlink(file_path)
        with sqlite3.connect('admins.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM image_descriptions WHERE filename = ?", (filename,))
            conn.commit()
        flash('Image deleted successfully!')
    else:
        flash('Image not found or invalid.')
    return redirect(url_for('admin'))

@app.route('/description/<filename>', methods=['POST'])
def save_description(filename):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    description = request.form.get('description', '').strip()
    if not allowed_file(filename):
        flash('Invalid image file.')
        return redirect(url_for('admin'))
    with sqlite3.connect('admins.db') as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO image_descriptions (filename, description) VALUES (?, ?)",
                  (filename, description))
        conn.commit()
    flash('Description saved successfully!')
    return redirect(url_for('admin'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)