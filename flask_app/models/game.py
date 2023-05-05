from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash, request

import re

import os

REGEX = re.compile(r'^[a-zA-z][a-zA-z\s]+$')

db = os.getenv("db_name")

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
    def delete(cls, data):
        query = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete_update_wins(cls, game_id, wins):
        wins = wins - 1
        wins = {
            "wins" : wins
        }
        query = "DELETE FROM games WHERE id = %(id)s;"
        query2 = "UPDATE teams SET wins = %(wins)s"
        return connectToMySQL(db).query_db(query, game_id), connectToMySQL(db).query_db(query2, wins)
    
    @classmethod
    def delete_update_losses(cls, game_id, losses):
        losses = losses - 1
        losses = {
            "losses" : losses
        }
        query = "DELETE FROM games WHERE id = %(id)s;"
        query2 = "UPDATE teams SET losses = %(losses)s"
        return connectToMySQL(db).query_db(query, game_id), connectToMySQL(db).query_db(query2, losses)

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) 
    
    @classmethod
    def update(cls, data):
        previous_win_loss = data['win_loss']
        if int(data['our_runs']) > int(data['their_runs']):
            win_loss = "W"
        elif int(data['our_runs']) < int(data['their_runs']):
            win_loss = "L"
        query_data = {
            "vs" : data['vs'],
            "home_or_away" : data['home_or_away'],
            "date" : data['date'],
            "time" : data['time'],
            "our_runs" : data['our_runs'],
            "their_runs" : data['their_runs'],
            "win_loss" : win_loss,
            "team_id" : data['team_id'],
            "id" : data['id']
        }
        if previous_win_loss == win_loss:
            query = "UPDATE games SET vs = %(vs)s, home_or_away = %(home_or_away)s, date = %(date)s, time = %(time)s, our_runs = %(our_runs)s, their_runs = %(their_runs)s, win_loss = %(win_loss)s, team_id = %(team_id)s WHERE id = %(id)s;" 
            return connectToMySQL(db).query_db(query, query_data)
        elif previous_win_loss == '0':
            if int(data['our_runs']) > int(data['their_runs']):
                team_wins = int(data['team_wins']) + 1
                query_data_WLT = {
                "wins" : team_wins,
                "team_id" : data['team_id']
                }
                query = "UPDATE teams SET wins = %(wins)s WHERE id = %(team_id)s;"
                query2 = "UPDATE games SET vs = %(vs)s, home_or_away = %(home_or_away)s, date = %(date)s, time = %(time)s, our_runs = %(our_runs)s, their_runs = %(their_runs)s, win_loss = %(win_loss)s, team_id = %(team_id)s WHERE id = %(id)s;"  
                return connectToMySQL(db).query_db(query, query_data_WLT), connectToMySQL(db).query_db(query2, query_data)
            elif int(data['our_runs']) < int(data['their_runs']):
                team_losses = int(data['team_losses']) + 1
                query_data_WLT = {
                    "losses" : team_losses,
                    "team_id" : data['team_id']
                }
                query = "UPDATE teams SET losses = %(losses)s WHERE id = %(team_id)s;" 
                query2 = "UPDATE games SET vs = %(vs)s, home_or_away = %(home_or_away)s, date = %(date)s, time = %(time)s, our_runs = %(our_runs)s, their_runs = %(their_runs)s, win_loss = %(win_loss)s, team_id = %(team_id)s WHERE id = %(id)s;"  
                return connectToMySQL(db).query_db(query, query_data_WLT), connectToMySQL(db).query_db(query2, query_data)
        elif previous_win_loss != win_loss:
            if int(data['our_runs']) > int(data['their_runs']):
                team_wins = int(data['team_wins']) + 1
                team_losses = int(data['team_losses']) - 1
                query_data_WLT = {
                "wins" : team_wins,
                "losses" : team_losses,
                "team_id" : data['team_id']
                }
                query = "UPDATE teams SET wins = %(wins)s, losses = %(losses)s WHERE id = %(team_id)s;"
                query2 = "UPDATE games SET vs = %(vs)s, home_or_away = %(home_or_away)s, date = %(date)s, time = %(time)s, our_runs = %(our_runs)s, their_runs = %(their_runs)s, win_loss = %(win_loss)s, team_id = %(team_id)s WHERE id = %(id)s;"  
                return connectToMySQL(db).query_db(query, query_data_WLT), connectToMySQL(db).query_db(query2, query_data)
            elif int(data['our_runs']) < int(data['their_runs']):
                team_losses = int(data['team_losses']) + 1
                team_wins = int(data['team_wins']) - 1
                query_data_WLT = {
                    "wins" : team_wins,
                    "losses" : team_losses,
                    "team_id" : data['team_id']
                }
                query = "UPDATE teams SET wins = %(wins)s, losses = %(losses)s WHERE id = %(team_id)s;" 
                query2 = "UPDATE games SET vs = %(vs)s, home_or_away = %(home_or_away)s, date = %(date)s, time = %(time)s, our_runs = %(our_runs)s, their_runs = %(their_runs)s, win_loss = %(win_loss)s, team_id = %(team_id)s WHERE id = %(id)s;"  
                return connectToMySQL(db).query_db(query, query_data_WLT), connectToMySQL(db).query_db(query2, query_data)