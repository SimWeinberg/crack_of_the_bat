from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash

# db = 'your_db_here'

class Game:
    def __init__(self, data):
        self.id = data['id']
        self.vs = data['vs']
        self.home_or_away = data['home_or_away']
        self.date = data['date']
        self.time = data['time']
        self.our_runs = data['our_runs']
        self.their_runs = data['their_runs']
        self.win_loss = data['win_loss']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team_id = data['team_id']