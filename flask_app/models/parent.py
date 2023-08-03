from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash, request

import re

import os

REGEX = re.compile(r'^[a-zA-z]+$')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app.models import team

db = os.getenv("db_name")

class Parent:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.force_reset = data['force_reset']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.teams = []

    @staticmethod
    def validate(parent):
        is_valid = True
        parent_name = [parent['first_name'], parent['last_name']]
        for i in parent_name:
            if not (len(i) >= 1 and len(i) <= 15):
                flash("Name must be 1-15 letters")
                is_valid = False
            if not REGEX.match(i): 
                flash("Name must be letters")
                is_valid = False
        if not EMAIL_REGEX.match(parent['email']): 
            flash("Invalid email address")
            is_valid = False
        if not (len(parent['password']) >= 8 and len(parent['password']) <= 15):
            flash("Password must be 8-15 characters")
            is_valid = False
        pword = parent['password']
        pwordc = parent['confirm_password']
        if not pword == pwordc:
            is_valid = False
            flash("Password does not match password confirmation")
        return is_valid
    
    @staticmethod
    def validate_reset(parent):
        is_valid = True
        if not (len(parent['password']) >= 8 and len(parent['password']) <= 15):
            flash("Password must be 8-15 characters")
            is_valid = False
        pword = parent['password']
        pwordc = parent['confirm_password']
        if not pword == pwordc:
            is_valid = False
            flash("Password does not match password confirmation")
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO parents (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        query2 = "INSERT INTO teams_has_parents (parent_id, team_id) SELECT (SELECT MAX(id) FROM parents), %(team_id)s;"
        return connectToMySQL(db).query_db(query, data), connectToMySQL(db).query_db(query2, data)
    
    @classmethod
    def add_team(cls, data):
        query = "UPDATE parents SET password = %(password)s, force_reset = 1 WHERE id = %(parent_id)s;"
        query2 = "INSERT INTO teams_has_parents (parent_id, team_id) VALUES (%(parent_id)s, %(team_id)s);"
        return connectToMySQL(db).query_db(query, data), connectToMySQL(db).query_db(query2, data)
    
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM parents WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) 
    
    @classmethod
    def update(cls, data):
        query = "UPDATE parents SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM teams_has_parents WHERE parent_id = %(id)s;"
        query2 = "DELETE FROM parents WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data), connectToMySQL(db).query_db(query2, data)
    
    @classmethod
    def get_parent_and_teams(cls, data):
        query = "SELECT * FROM parents LEFT JOIN teams_has_parents ON parents.id = teams_has_parents.parent_id LEFT JOIN teams ON teams.id = teams_has_parents.team_id WHERE parents.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        parent = cls(results[0])
        for row in results:
            team_data = {
                "id" : row['teams.id'],
                "name" : row['name'],
                "year" : row['year'],
                "wins" : row['wins'],
                "losses" : row['losses'],
                "created_at" : row['teams.created_at'],
                "updated_at" : row['teams.updated_at'],
                "parent_id" : row['parent_id'],
                "coach_id" : row['coach_id'],
            }
            parent.teams.append(team.Team(team_data))
        return parent
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM parents WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def create_image(cls, data):
        query = "UPDATE parents SET image_path = %(image_path)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def reset_password(cls, data):
        query = "UPDATE parents SET password = %(password)s, force_reset = 0 WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_parent(cls, data):
        query = "SELECT * FROM parents WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])