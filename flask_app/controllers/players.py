from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash 

from flask_app.models.player import Player

from flask_app.models.coach import Coach

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/Simcha/Documents/Python/projects_and_algorithms/crack_of_the_bat/flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/player/add/<int:id>')
def player_add(id):
    if not 'user_id' in session:
        return redirect('/')
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('player_add.html', team_id = id, coach = Coach.get_coach(coach_id))

@app.route('/player/create', methods=['POST'])
def player_create():
    if not 'user_id' in session:
        return redirect('/')
    if not Player.validate(request.form):
        id = request.form['team_id']
        return redirect(f'/player/add/{id}')
    Player.save(request.form)
    id = request.form['team_id']
    return redirect(f'/team/view/{id}')

@app.route('/player/edit/<int:id>')
def player_edit(id):
    if not 'user_id' in session:
        return redirect('/')
    player_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('player_edit.html', player = Player.get_one(player_id), coach = Coach.get_coach(coach_id))

@app.route('/player/update', methods=['POST'])
def player_update():
    if not 'user_id' in session:
        return redirect('/')
    if not Player.validate(request.form):
            id = request.form['id']
            return redirect(f'/player/edit/{id}')
    Player.update(request.form)
    id = request.form['team_id']
    return redirect(f'/team/view/{id}')

@app.route('/player/edit/stats/<int:id>')
def player_edit_stats(id):
    if not 'user_id' in session:
        return redirect('/')
    player_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('player_edit_stats.html', player = Player.get_one(player_id), coach = Coach.get_coach(coach_id))

@app.route('/player/update/stats', methods=['POST'])
def player_update_stats():
    if not 'user_id' in session:
        return redirect('/')
    if not Player.validate_update_stats(request.form):
            id = request.form['player_id']
            return redirect(f'/player/edit/stats/{id}')
    Player.calculate(request.form)
    id = request.form['team_id']
    return redirect(f'/team/view/{id}')

@app.route('/player/delete/<int:id>/<int:team_id>')
def delete_player(id, team_id):
    data = {
        "id" : id
    }
    Player.delete(data)
    return redirect(f'/team/view/{team_id}')

@app.route('/player/upload/pic/<int:id>')
def player_upload_pic(id):
    if not 'user_id' in session:
        return redirect('/')
    player_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('player_upload_pic.html', player = Player.get_one(player_id), coach = Coach.get_coach(coach_id))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/player/upload/pic/file', methods=['GET', 'POST'])
def player_upload_pic_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            id = request.form['id']
            return redirect(f'/player/upload/pic/{id}')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            id = request.form['id']
            return redirect(f'/player/upload/pic/{id}')
        if not allowed_file(file.filename):
            flash('Invalid file')
            id = request.form['id']
            return redirect(f'/player/upload/pic/{id}')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                "image_path" : '/static/images/'+filename,
                "id" : request.form['id']
            }
            Player.create_image(data)
        team_id = request.form['team_id']
        return redirect(f'/team/view/{team_id}')