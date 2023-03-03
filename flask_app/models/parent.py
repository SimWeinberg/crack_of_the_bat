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
        self.team_id = data['team_id']
        self.teams = []

    @staticmethod
    def validate(parent):
        print(parent['email'])
        is_valid = True
        parent_name = [parent['first_name'], parent['last_name']]
        for i in parent_name:
            if not (len(i) >= 1 and len(i) <= 15):
                flash("Name must be 1-15 letters")
                is_valid = False
            if not REGEX.match(i): 
                flash("Name is letters only")
                is_valid = False
        query = "SELECT * FROM parents WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, parent)
        if len(results) >= 1:
            flash("Email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(parent['email']): 
            flash("Invalid email address")
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO parents (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
        return connectToMySQL(db).query_db(query, data)