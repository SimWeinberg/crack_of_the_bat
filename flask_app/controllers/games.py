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

@app.route('/game/edit/<int:id>/<int:team_id>/<win_loss>')
def game_edit(id, team_id, win_loss):
    if not 'user_id' in session:
        return redirect('/')
    if (win_loss == "W") or (win_loss == "L") or (win_loss == "T"):
        game_id = {
            "id" : id
        }
        team_id = {
            "id" : team_id
        }
        coach_id = {
            "id" : session['user_id']
        }
        return render_template('game_edit2.html', game = Game.get_one(game_id), coach = Coach.get_coach(coach_id))
    game_id = {
        "id" : id
    }
    team_id = {
        "id" : team_id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('game_edit.html', game = Game.get_one(game_id), coach = Coach.get_coach(coach_id), team = Team.get_one(team_id))
        
@app.route('/game/update', methods=['POST'])
def game_update():
    if not 'user_id' in session:
        return redirect('/')
    if not Game.validate(request.form):
            id = request.form['id']
            team_id = request.form['team_id']
            win_loss = request.form['win_loss']
            return redirect(f'/game/edit/{id}/{team_id}/{win_loss}')
    Game.update(request.form)
    Team.get_record(request.form)
    id = request.form['team_id']
    return redirect(f'/games/view/{id}')

@app.route('/game/update2', methods=['POST'])
def game_update2():
    if not 'user_id' in session:
        return redirect('/')
    if not Game.validate(request.form):
            id = request.form['id']
            team_id = request.form['team_id']
            win_loss = request.form['win_loss']
            return redirect(f'/game/edit/{id}/{team_id}/{win_loss}')
    Game.update(request.form)
    id = request.form['team_id']
    return redirect(f'/games/view/{id}')

@app.route('/game/delete/<int:id>/<int:team_id>/<int:wins>/<int:losses>/<win_loss>')
def delete_game(id, team_id, wins, losses, win_loss):
    game_id = {
        "id" : id
    }
    if win_loss == "W":
        Game.delete_update_wins(game_id, wins)
        return redirect(f'/games/view/{team_id}')
    elif win_loss == "L":
        Game.delete_update_losses(game_id, losses)
        return redirect(f'/games/view/{team_id}')
    Game.delete(game_id)
    return redirect(f'/games/view/{team_id}')