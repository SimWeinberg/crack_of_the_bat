from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash 

from flask_app.models.team import Team

from flask_app.models.coach import Coach

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