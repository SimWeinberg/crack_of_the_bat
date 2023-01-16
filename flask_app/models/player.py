from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash, request

import re

REGEX = re.compile(r'^[0-9]+$')

# db = 'your_db_here'

class Player:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.position = data['position']
        self.avg = data['avg']
        self.obp = data['obp']
        self.slg = data['slg']
        self.era = data['era']
        self.hits = data['hits']
        self.at_bats = data['at_bats']
        self.walks = data['walks']
        self.hit_by_pitch = data['hit_by_pitch']
        self.sacrifice_flies = data['sacrifice_flies']
        self.total_innings = data['total_innings']
        self.total_bases = data['total_bases']
        self.earned_runs = data['earned_runs']
        self.innings_pitched = data['innings_pitched']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team_id = data['team_id']
    
    @staticmethod
    def validate(player):
        is_valid = True
        player = [player['first_name'], player['last_name']]
        for i in player:
            if len(i) < 1:
                flash("Name must be at least 1 letter")
                is_valid = False
            if REGEX.match(i): 
                flash("Name is letters only")
                is_valid = False
        return is_valid

    @staticmethod
    def validate_update_stats(player):
        is_valid = True
        stats = [player['hits'], player['at_bats'], player['walks'], player['hit_by_pitch'], player['sacrifice_flies'], player['total_bases']]
        for i in stats:
            if len(i) < 1:
                flash("Stat must be at least 1 number")
                is_valid = False
        if request.form['position'] == 'P':
            statsPitcher = [player['total_innings'], player['total_innings']]
            for i in statsPitcher:
                if len(i) < 1:
                    flash("Stat must be at least 1 number")
                    is_valid = False
            if len(player['innings_pitched']) < .33:
                flash("Innings pitched must be at least .33")
                is_valid = False 
        return is_valid
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO players (first_name, last_name, position, team_id) VALUES (%(first_name)s, %(last_name)s, %(position)s, %(team_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM players WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM players WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) 

    @classmethod
    def calculate(cls, data):
        hits = (int(data['previous_hits']) + int(data['hits'])) 
        at_bats = (int(data['previous_at_bats']) + int(data['at_bats']))
        walks = (int(data['previous_walks']) + int(data['walks']))
        hit_by_pitch = (int(data['previous_hit_by_pitch']) + int(data['hit_by_pitch']))
        sacrifice_flies = (int(data['previous_sacrifice_flies']) + int(data['sacrifice_flies']))
        total_bases = (int(data['previous_total_bases']) + int(data['total_bases']))
        if data['position'] == 'P':
            total_innings = (int(data['previous_total_innings']) + int(data['total_innings']))
            earned_runs = (int(data['previous_earned_runs']) + int(data['earned_runs']))
            innings_pitched = ((float(data['previous_innings_pitched'])) + float(data['innings_pitched']))
            era = (earned_runs * total_innings) /  innings_pitched
        avg = hits / at_bats
        obp = (hits + walks + hit_by_pitch) / (at_bats + walks + hit_by_pitch + sacrifice_flies)
        slg = total_bases / at_bats
        if data['position'] == 'P':
            query_data = {
                "hits" : hits,
                "at_bats" : at_bats,
                "walks" : walks,
                "hit_by_pitch" : hit_by_pitch,
                "sacrifice_flies" : sacrifice_flies,
                "total_bases" : total_bases,
                "total_innings" : total_innings,
                "earned_runs" : earned_runs,
                "innings_pitched" :innings_pitched,
                "avg" : avg,
                "obp" : obp,
                "slg" : slg,
                "era" : era,
                "player_id" : data['player_id']
            }
            query = "UPDATE players SET hits = %(hits)s, at_bats = %(at_bats)s, walks = %(walks)s, hit_by_pitch = %(hit_by_pitch)s, sacrifice_flies = %(sacrifice_flies)s, total_bases = %(total_bases)s, total_innings = %(total_innings)s, earned_runs = %(earned_runs)s, innings_pitched = %(innings_pitched)s, avg = ROUND(%(avg)s, 3), obp = ROUND(%(obp)s, 3), slg = ROUND(%(slg)s, 3), era = ROUND(%(era)s, 2) WHERE id = %(player_id)s;"
            return connectToMySQL(db).query_db(query, query_data)
        else:
            query_data = {
                "hits" : hits,
                "at_bats" : at_bats,
                "walks" : walks,
                "hit_by_pitch" : hit_by_pitch,
                "sacrifice_flies" : sacrifice_flies,
                "total_bases" : total_bases,
                "avg" : avg,
                "obp" : obp,
                "slg" : slg,
                "player_id" : data['player_id']
            }
            query = "UPDATE players SET hits = %(hits)s, at_bats = %(at_bats)s, walks = %(walks)s, hit_by_pitch = %(hit_by_pitch)s, sacrifice_flies = %(sacrifice_flies)s, total_bases = %(total_bases)s, avg = ROUND(%(avg)s, 3), obp = ROUND(%(obp)s, 3), slg = ROUND(%(slg)s, 3) WHERE id = %(player_id)s;"
            return connectToMySQL(db).query_db(query, query_data)

    @classmethod
    def update(cls, data):
        query = "UPDATE players SET first_name = %(first_name)s, last_name = %(last_name)s, position = %(position)s  WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def create_image(cls, data):
        query = "UPDATE players SET image_path = %(image_path)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)