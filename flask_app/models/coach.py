from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash

import re

REGEX = re.compile(r'^[a-zA-z]+$')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app.models import team

db = ''

class Coach:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.image_path = data['image_path']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.teams = []

    @staticmethod
    def validate(coach):
        is_valid = True
        coach_name = [coach['first_name'], coach['last_name']]
        for i in coach_name:
            if not REGEX.match(i):
                flash("Name must be letters")
                is_valid = False
            if not (len(i) >= 2 and len(i) <= 15):
                flash("Name must be 2-15 letters")
                is_valid = False
        query = "SELECT * FROM coachs WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, coach)
        if len(results) >= 1:
            flash("Email already taken")
            is_valid=False
        if not EMAIL_REGEX.match(coach['email']): 
            flash("Invalid email address")
            is_valid = False
        if not (len(coach['password']) >= 8 and len(coach['password']) <= 15):
            flash("Password must be 8-15 characters")
            is_valid = False
        pword = coach['password']
        pwordc = coach['confirm_password']
        if not pword == pwordc:
            is_valid = False
            flash("Password does not match password confirmation")
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO coachs (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_coach_and_teams(cls, data):
        query = "SELECT * FROM coachs LEFT JOIN teams ON coachs.id = teams.coach_id WHERE coachs.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        coach = cls(results[0])
        for row in results:
            if row['teams.id'] == None:
                break
            team_data = {
                "id" : row['teams.id'],
                "name" : row['name'],
                "year" : row['year'],
                "wins" : row['wins'],
                "losses" : row['losses'],
                "created_at" : row['teams.created_at'],
                "updated_at" : row['teams.updated_at'],
                "coach_id" : row['coach_id'],
            }
            coach.teams.append(team.Team(team_data))
        return coach

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM coachs WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_image(cls, data):
        query = "UPDATE coachs SET image_path = %(image_path)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_coach(cls, data):
        query = "SELECT * FROM coachs WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])