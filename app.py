from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
import json
import threading

from job_model import Job
import queue_manager
import job_runner

# App setup
app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'hash', 'md5', 'sha1'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Wordlist/Rule dirs
os.makedirs('wordlists', exist_ok=True)
os.makedirs('rules', exist_ok=True)

# Load users
with open('users.json') as f:
    USERS = json.load(f)

# Load or initialize queue
jobs = queue_manager.load_queue()
queue_lock = threading.Lock()

# Start job runner
job_runner.start_runner(jobs, queue_lock)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USERS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    wordlist_files = os.listdir('wordlists')
    rule_files = os.listdir('rules')

    if request.method == 'POST':
        hash_file = request.files.get('hash_file')
        hash_type = request.form.get('hash_type')
        wordlist = request.form.get('wordlist')
        rule = request.form.get('rule')

        if not hash_file or not allowed_file(hash_file.filename):
            flash("Invalid or missing hash file", "danger")
            return redirect(url_for('dashboard'))

        filename = secure_filename(hash_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        hash_file.save(filepath)

        new_job = Job(
            username=session['username'],
            hash_file=filename,
            hash_type=hash_type,
            wordlist=wordlist,
            rule=rule if rule else None
        )

        with queue_lock:
            jobs.append(new_job)
            queue_manager.save_queue(jobs)

        flash(f"Job submitted successfully! ID: {new_job.id}", "success")

    with queue_lock:
        user_jobs = [j.to_dict() for j in jobs if j.username == session['username']]

    return render_template('dashboard.html',
                           username=session['username'],
                           wordlists=wordlist_files,
                           rules=rule_files,
                           jobs=user_jobs)

if __name__ == '__main__':
    app.run(debug=True)
