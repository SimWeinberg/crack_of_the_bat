from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash 

from flask_app.models.team import Team

from flask_app.models.coach import Coach

@app.route('/team/add')
def team_add():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('team_add.html', coach = Coach.get_coach(data))

@app.route('/team/create', methods=['POST'])
def team_create():
    if not 'user_id' in session:
        return redirect('/')
    if not Team.validate(request.form):
        return redirect('/team/add')
    Team.save(request.form)
    return redirect('/coach/dashboard')

@app.route('/team/view/<int:id>')
def team_view(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('team_view.html', team = Team.get_team_and_players(team_id), coach = Coach.get_coach(coach_id))

@app.route('/team/edit/<int:id>')
def team_edit(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('team_edit.html', team = Team.get_one(team_id), coach = Coach.get_coach(coach_id))

@app.route('/team/update', methods=['POST'])
def team_update():
    if not 'user_id' in session:
        return redirect('/')
    if not Team.validate(request.form):
        id = request.form['id']
        return redirect(f'/team/edit/{id}')
    Team.edit(request.form)
    return redirect('/coach/dashboard')

@app.route('/team/delete/warning/<int:id>')
def team_delete_warning(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('team_delete_warning.html', team = Team.get_team_and_players(team_id), games = Team.get_team_and_games(team_id), coach = Coach.get_coach(coach_id))

@app.route('/team/delete/<int:id>')
def team_delete(id):
    data = {
        "id" : id
    }
    Team.delete_players(data)
    Team.delete_games(data)
    Team.delete(data)
    return redirect('/coach/dashboard')