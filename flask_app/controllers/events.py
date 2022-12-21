from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask import flash
from flask_app import app
from flask import Flask, redirect, render_template, request, session
from datetime import datetime
dateFormat = "%m/%d/%Y"

@app.route('/event/map_event/<int:event_id>')
def map_form(event_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : event_id
    }    
    return render_template("map_event.html", event = Event.get_by_id(data), messages = Message.get_by_id(data), date = dateFormat )
    

@app.route('/event/search_event')
def search_event_form():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    return render_template('search_event.html', events = Event.get_all_events_with_user())

@app.route('/event/search_by_type/', methods=['POST'])
def search_event_type():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'event_type' : request.form['event_type']
    }
    
    return render_template('search_list.html', events = Event.get_all_events_with_user_by_event_type(data))

@app.route('/event/search_by_location/', methods=['POST'])
def search_event_location():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'location' : request.form['location']
    }
    
    return render_template('search_list.html', events = Event.get_all_events_with_user_by_event_location(data))

@app.route('/event/search_by_date/', methods=['POST'])
def search_event_date():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'event_date' : request.form['event_date']
    }
    
    return render_template('search_list.html', events = Event.get_all_events_with_user_by_event_date(data))


@app.route('/event/add_event')
def add_event_form():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : session['user_id']
    }
    
    return render_template('add_event.html')

@app.route('/event/create', methods=['POST'])
def create_event():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Event.event_validator(request.form):
        return redirect('/event/add_event')
    
            
    data = {
        'event_type' : request.form['event_type'],
        'location' : request.form['location'],
        'spots_open' : request.form['spots_open'],
        'event_date' : request.form['event_date'],
        'event_time' : request.form['event_time'],
        'user_id' : session['user_id'] 
    }
    
    Event.create_event(data)
    return redirect('/dashboard')
    
   

@app.route('/event/edit_event/<int:event_id>')
def edit_event(event_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : event_id
    }    
    return render_template("edit_event.html", event = Event.get_one(data))

@app.route('/event/update/<int:event_id>', methods=['POST'])
def update_event(event_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    valid = Event.event_validator(request.form)
    if valid:
        Event.update_event(request.form)
        return redirect('/dashboard')
    
    return redirect(f"/event/edit_event/{event_id}")

@app.route('/event/delete_event/<int:event_id>')
def delete_event(event_id):    
    if 'user_id' not in session:
        return redirect('/logout')    
    data = {
        'id' : event_id
    }
    Event.delete_event(data)
    return redirect('/dashboard')

@app.route('/event/<int:event_id>')
def display_event(event_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : event_id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('view_event.html', event = Event.get_by_id(data), date = dateFormat)



