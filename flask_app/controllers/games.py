from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash 

from flask_app.models.team import Team

from flask_app.models.coach import Coach

from flask_app.models.game import Game

@app.route('/games/view/<int:id>')
def games_view(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('games_view.html', team = Team.get_team_and_games(team_id), coach = Coach.get_coach(coach_id))

@app.route('/game/add/<int:id>')
def game_add(id):
    if not 'user_id' in session:
        return redirect('/')
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('game_add.html', team_id = id, coach = Coach.get_coach(coach_id))

@app.route('/game/create', methods=['POST'])
def game_create():
    if not 'user_id' in session:
        return redirect('/')
    if not Game.validate(request.form):
        id = request.form['team_id']
        return redirect(f'/game/add/{id}')
    Game.save(request.form)
    id = request.form['team_id']
    return redirect(f'/games/view/{id}')

@app.route('/game/edit/<int:id>')
def game_edit(id):
    if not 'user_id' in session:
        return redirect('/')
    game_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('game_edit.html', game = Game.get_one(game_id), coach = Coach.get_coach(coach_id))

@app.route('/game/update', methods=['POST'])
def game_update():
    if not 'user_id' in session:
        return redirect('/')
    if not Game.validate(request.form):
            id = request.form['id']
            return redirect(f'/game/edit/{id}')
    Game.update(request.form)
    id = request.form['team_id']
    return redirect(f'/games/view/{id}')