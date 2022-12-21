from flask import  render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
from datetime import date
dateFormat = "%m/%d/%Y"

@app.route('/user/account/<int:event_id>')
def account_info(event_id):
    data = {
        'id' : event_id
    }
    return render_template('user_account.html', event = Event.get_by_id(data))

           

@app.route('/')
def index():
    
    return render_template('new_user.html')

@app.route('/register', methods=['POST'])
def register():
    
    if not User.user_register(request.form):
        return redirect('/')
    
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "pwd" : bcrypt.generate_password_hash(request.form['pwd'])
    }
    
    id = User.save(data)
    session['user_id'] = id    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.pwd, request.form['pwd']):
        flash("Invalid Password", "login")
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : session['user_id']
    }
    
    return render_template("dashboard.html", events = Event.get_all_events_with_user(), user = User.get_by_id(data), today = date.today(),  date = dateFormat)

@app.route('/logout')
def logout():
    
    session.clear()
    return redirect('/')
