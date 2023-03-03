from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash 

from flask_app.models.parent import Parent

from flask_app.models.coach import Coach

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
    return redirect(f'/team/view/{id}')