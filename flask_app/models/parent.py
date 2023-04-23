from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app

from flask import flash, request

import re

REGEX = re.compile(r'^[a-zA-z]+$')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = ''

class Parent:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
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
                flash("Name is letters only")
                is_valid = False
        if not EMAIL_REGEX.match(parent['email']): 
            flash("Invalid email address")
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO parents (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
        query2 = "INSERT INTO teams_has_parents (parent_id, team_id) SELECT (SELECT MAX(id) FROM parents), %(team_id)s;"
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