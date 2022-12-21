from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask import flash
from flask_app import app
from flask import Flask, redirect, render_template, request, session
from datetime import datetime
dateFormat = "%m/%d/%Y"

@app.route('/message/create/<int:event_id>', methods=['POST'])
def create_message(event_id):
    
    if 'user_id' not in session:
        return redirect('/logout')    
            
    data = {
        
        'event_id' : event_id
        
    }
    
    Message.create_message(data)
    return redirect('/dashboard')
    