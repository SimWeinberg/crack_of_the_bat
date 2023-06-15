from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash

from flask_app.models.parent import Parent

from flask_app.models.coach import Coach

from flask_app.models.team import Team

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

import requests

import os

@app.route('/parent/login', methods=['POST'])
def parent_login():
    data = { 
        "email" : request.form['email'] 
    }
    user_in_db = Parent.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    if user_in_db.force_reset == True:
        return redirect('/parent/reset')
    return redirect('/parent/dashboard')

@app.route('/parent/reset')
def parent_reset():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('parent_reset_password.html', parent = Parent.get_one(data))

@app.route('/parent/reset_password', methods=['POST'])
def parent_reset_password():
    if not 'user_id' in session:
        return redirect('/')
    if not Parent.validate_reset(request.form):
        return redirect('/parent/reset')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "password" : pw_hash,
        "id" : request.form['id']
    }
    Parent.reset_password(data)
    return redirect('/parent/dashboard')

@app.route('/parent/dashboard')
def parent_dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('parent_dashboard.html', parent_and_teams = Parent.get_parent_and_teams(data))

@app.route('/parent/team/view/<int:id>')
def parent_team_view(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = {
        "id" : id
    }
    parent_id = {
        "id" : session['user_id']
    }
    return render_template('team_view.html', team = Team.get_team_and_players(team_id), parent = Parent.get_one(parent_id))

@app.route('/parents/view/<int:id>')
def parents_view(id):
    if not 'user_id' in session:
        return redirect('/')
    team_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('parents_view.html', team = Team.get_team_and_parents(team_id), coach = Coach.get_coach(coach_id))

@app.route('/parent/add/<int:id>')
def parent_add(id):
    if not 'user_id' in session:
        return redirect('/')
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('parent_add.html', team_id = id, coach = Coach.get_coach(coach_id))

@app.route('/parent/create', methods=['POST'])
def parent_create():
    if not 'user_id' in session:
        return redirect('/')
    if not Parent.validate(request.form):
        id = request.form['team_id']
        return redirect(f'/parent/add/{id}')
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    parent_email = request.form['email']
    password = request.form['password']
    # requests.post(
	# 	"https://api.mailgun.net/v3/sandbox0b439f2fb6364e88a24fba49512319f8.mailgun.org/messages",
	# 	auth=("api", os.getenv("api_key")),
	# 	data={"from": "Mailgun Sandbox <postmaster@sandbox0b439f2fb6364e88a24fba49512319f8.mailgun.org>",
	# 		"to": parent_email,
	# 		"subject": "Welcome to Crack of The Bat!",
	# 		"text": f"Congratulations {first_name}, you have been added as a parent to team_here year_here!  Please login and reset your password.  Current password is {password}."})
    requests.post(
		"https://api.mailgun.net/v3/sandbox0b439f2fb6364e88a24fba49512319f8.mailgun.org/messages",
		auth=("api", os.getenv("api_key")),
		data={"from": "Mailgun Sandbox <postmaster@sandbox0b439f2fb6364e88a24fba49512319f8.mailgun.org>",
			"to": parent_email,
			"subject": "Welcome to Crack of The Bat!",
			"template": "parent_add"})
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    email = {
        "email" : request.form['email']
    }
    user_in_db = Parent.get_by_email(email)
    if not user_in_db:
        data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
        "team_id" : request.form['team_id']
    }
        Parent.save(data)
        id = request.form['team_id']
        return redirect(f'/parents/view/{id}')
    elif user_in_db:
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "password" : pw_hash,
            "team_id" : request.form['team_id'],
            "parent_id" : user_in_db.id
        }
        Parent.add_team(data)
        team_id = request.form['team_id']
        return redirect(f'/parents/view/{team_id}')

@app.route('/parent/edit/<int:id>/<int:team_id>')
def parent_edit(id, team_id):
    if not 'user_id' in session:
        return redirect('/')
    parent_id = {
        "id" : id
    }
    coach_id = {
        "id" : session['user_id']
    }
    return render_template('parent_edit.html', parent = Parent.get_one(parent_id), coach = Coach.get_coach(coach_id), team = team_id)

@app.route('/parent/update', methods=['POST'])
def parent_update():
    if not 'user_id' in session:
        return redirect('/')
    if not Parent.validate(request.form):
            id = request.form['id']
            return redirect(f'/parent/edit/{id}')
    Parent.update(request.form)
    id = request.form['team_id']
    return redirect(f'/parents/view/{id}')

@app.route('/parent/delete/<int:id>/<int:team_id>')
def delete_parent(id, team_id):
    data = {
        "id" : id
    }
    Parent.delete(data)
    return redirect(f'/parents/view/{team_id}')