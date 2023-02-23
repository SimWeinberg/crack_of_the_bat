from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash, request

import re

REGEX = re.compile(r'^[a-zA-z][a-zA-z\s]+$')

db = ''

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

    @staticmethod
    def validate(game):
        is_valid = True
        if not REGEX.match(game['vs']):
            flash("vs must be letters")
            is_valid = False
        if not (len(game['vs']) >=3 and len(game['vs']) <= 20):
            flash("vs must be 3-20 letters")
            is_valid = False
        if (len(game)) == 5:
            game_data = [game['vs'], game['date'], game['time']]
            for i in game_data:
                if len(i) < 1:
                    flash("Must enter data")
                    is_valid = False
        if (len(game)) > 5:
            game_data_edit = [game['vs'], game['date'], game['time'], game['our_runs'], game['their_runs']]
            for i in game_data_edit:
                if len(i) < 1:
                    flash("Must enter data")
                    is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO games (vs, home_or_away, date, time, team_id) VALUES (%(vs)s, %(home_or_away)s, %(date)s, %(time)s, %(team_id)s);"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) 
    
    @classmethod
    def update(cls, data):
        query = "UPDATE games SET vs = %(vs)s, home_or_away = %(home_or_away)s, date = %(date)s, time = %(time)s, our_runs = %(our_runs)s, their_runs = %(their_runs)s, win_loss = %(win_loss)s, team_id = %(team_id)s WHERE id = %(id)s;" 
        return connectToMySQL(db).query_db(query, data)