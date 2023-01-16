from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash

from flask_app.models.coach import Coach

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/Simcha/Documents/Python/projects_and_algorithms/crack_of_the_bat/flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def registration():
    return render_template('registration.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register/coach', methods=['POST'])
def register_coach():
    if not Coach.validate_registration(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    id = Coach.save(data)
    session['user_id'] = id
    return redirect('/coach/dashboard') 

@app.route('/login/coach', methods=['POST'])
def login_coach():
    data = { 
        "email" : request.form['email'] 
    }
    user_in_db = Coach.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/coach/dashboard')

@app.route('/coach/dashboard')
def coach_dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('coach_dashboard.html', coach_and_teams = Coach.get_coach_and_teams(data))

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/coach/upload/pic')
def coach_upload_pic():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('coach_upload_pic.html', coach = Coach.get_coach(data))

@app.route('/coach/upload/pic/<int:id>')
def coach_upload_pic_from_team_view(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = id
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('coach_upload_pic_from_team_view.html', coach = Coach.get_coach(coach_id), team_id = team_id)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/coach/upload/pic/file', methods=['GET', 'POST'])
def coach_upload_pic_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            if request.form['team_id']:
                team_id = request.form['team_id']
                return redirect(f'/coach/upload/pic/{team_id}')
            return redirect('/coach/upload/pic')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            if request.form['team_id']:
                team_id = request.form['team_id']
                return redirect(f'/coach/upload/pic/{team_id}')
            return redirect('/coach/upload/pic')
        if not allowed_file(file.filename):
            flash('Invalid file')
            if request.form['team_id']:
                team_id = request.form['team_id']
                return redirect(f'/coach/upload/pic/{team_id}')
            return redirect('/coach/upload/pic')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                "image_path" : '/static/images/'+filename,
                "id" : session['user_id']
            }
            Coach.create_image(data)
        if request.form['team_id']:
            team_id = request.form['team_id']
            return redirect(f'/team/view/{team_id}')
        return redirect('/coach/dashboard')