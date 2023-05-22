from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash 

from flask_app.models.parent import Parent

from flask_app.models.coach import Coach

from flask_app.models.team import Team

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

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
        return redirect('/parent/reset_password')
    return redirect('/parent/dashboard')

@app.route('/parent/reset_password')
def parent_reset_password():
    if not 'user_id' in session:
        return redirect('/')
    # data = {
    #     "id" : session['user_id']
    # }
    return render_template('parent_reset_password.html')

@app.route('/parent/dashboard')
def parent_dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template('parent_dashboard.html', parent_and_teams = Parent.get_parent_and_teams(data))

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
    Parent.save(request.form)
    id = request.form['team_id']
    return redirect(f'/parents/view/{id}')

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