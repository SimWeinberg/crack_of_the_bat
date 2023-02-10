from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash, session

import re

REGEX = re.compile(r'^[a-zA-z][a-zA-z\s]+$')

REGEX_YEAR = re.compile(r'^[2-9][0-9]+$')

from flask_app.models import player

from flask_app.models import game

db = 'your_db_here'

class Team:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.coach_id = data['coach_id']
        self.players = []
        self.games = []

    @staticmethod
    def validate(team):
        is_valid = True
        if not REGEX.match(team['name']):
            flash("Name must letters")
            is_valid = False
        if not (len(team['name']) >= 3 and len(team['name']) <= 15):
            flash("Name must be 3-15 letters")
            is_valid = False
        if len(team['year']) != 4:
            flash("Year must be 4 digits")
            is_valid = False
        if not REGEX_YEAR.match(team['year']): 
            flash("Invalid year")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO teams (name, year, coach_id) VALUES (%(name)s, %(year)s, %(coach_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM teams WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def edit(cls, data): 
        query = "UPDATE teams SET name = %(name)s, year = %(year)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_team_and_players(cls, data):
        query = "SELECT * FROM teams LEFT JOIN players ON teams.id = players.team_id WHERE teams.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        team = cls(results[0])
        for row in results:
            if row['players.id'] == None:
                break
            player_data = {
                "id" : row['players.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "position" : row['position'],
                "avg" : row['avg'],
                "obp" : row['obp'],
                "slg" : row['slg'],
                "era" : row['era'],
                "hits" : row['hits'],
                "at_bats" : row['at_bats'],
                "walks" : row['walks'],
                "hit_by_pitch" : row['hit_by_pitch'],
                "sacrifice_flies" : row['sacrifice_flies'],
                "total_innings" : row['total_innings'],
                "total_bases" : row['total_bases'],
                "earned_runs" : row['earned_runs'],
                "innings_pitched" : row['innings_pitched'],
                "image_path" : row['image_path'],
                "created_at" : row['players.created_at'],
                "updated_at" : row['players.updated_at'],
                "team_id" : row['team_id'],
            }
            team.players.append(player.Player(player_data))
        return team

    @classmethod
    def get_team_and_games(cls, data):
        query = "SELECT * FROM teams LEFT JOIN games ON teams.id = games.team_id WHERE teams.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        team = cls(results[0])
        for row in results:
            if row['games.id'] == None:
                break
            game_data = {
                "id" : row['id'],
                "vs" : row['vs'],
                "home_or_away" : row['home_or_away'],
                "date" : row['date'],
                "time" : row['time'],
                "our_runs" : row['our_runs'],
                "their_runs" : row['their_runs'],
                "win_loss" : row['win_loss'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "team_id" : row['team_id'],
            }
            team.games.append(game.Game(game_data))
        return team
    
    @classmethod
    def delete_players(cls, data):
        query = "DELETE FROM players WHERE team_id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM teams WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)