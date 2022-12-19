from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, redirect
from flask_app.models import user


class Event:
    def __init__(self, data):
        self.id = data['id']
        self.event_type = data['event_type']
        self.location = data['location']
        self.spots_open = data['spots_open']
        self.event_date = data['event_date']
        self.event_time = data['event_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        
    # Class method to Create
    @classmethod
    def create_event(cls, form_data):
        query = "INSERT INTO events (event_type, location, spots_open, event_date, event_time, user_id) VALUES (%(event_type)s, %(location)s, %(spots_open)s, %(event_date)s, %(event_time)s,  %(user_id)s);"
        return connectToMySQL('group_project_schema').query_db(query, form_data)
    
    # Class method to Retrieve (all) items
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        results = connectToMySQL('group_project_schema').query_db(query)
        events = []
        for event in results:
            events.append( cls(events) )
        return events
    
    # Method to Retrieve items with user data
    @classmethod
    def get_all_events_with_user(cls):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id;"
        events = connectToMySQL('group_project_schema').query_db(query)
        results = []
        for event in events:
            data = {
                'id' : event['users.id'],
                'first_name' : event['first_name'],
                'last_name' : event['last_name'],
                'email' : event['email'],
                'pwd' : event['pwd'],
                'created_at' : event['users.created_at'],
                'updated_at' : event['users.updated_at']
            }
            one_event = cls(event)
            one_event.creator = user.User(data)
            results.append(one_event) 
        return events
    
    @classmethod
    def get_all_events_with_user_by_event_type(cls, form_data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE event_type = %(event_type)s;"
        events = connectToMySQL('group_project_schema').query_db(query, form_data)
        results = []
        for event in events:
            data = {
                'id' : event['users.id'],
                'first_name' : event['first_name'],
                'last_name' : event['last_name'],
                'email' : event['email'],
                'pwd' : event['pwd'],
                'created_at' : event['users.created_at'],
                'updated_at' : event['users.updated_at']
            }
            one_event = cls(event)
            one_event.creator = user.User(data)
            results.append(one_event) 
        return events
    
    @classmethod
    def get_all_events_with_user_by_event_location(cls, form_data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE location = %(location)s;"
        events = connectToMySQL('group_project_schema').query_db(query, form_data)
        results = []
        for event in events:
            data = {
                'id' : event['users.id'],
                'first_name' : event['first_name'],
                'last_name' : event['last_name'],
                'email' : event['email'],
                'pwd' : event['pwd'],
                'created_at' : event['users.created_at'],
                'updated_at' : event['users.updated_at']
            }
            one_event = cls(event)
            one_event.creator = user.User(data)
            results.append(one_event) 
        return events
    
    @classmethod
    def get_all_events_with_user_by_event_date(cls, form_data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE event_date = %(event_date)s;"
        events = connectToMySQL('group_project_schema').query_db(query, form_data)
        results = []
        for event in events:
            data = {
                'id' : event['users.id'],
                'first_name' : event['first_name'],
                'last_name' : event['last_name'],
                'email' : event['email'],
                'pwd' : event['pwd'],
                'created_at' : event['users.created_at'],
                'updated_at' : event['users.updated_at']
            }
            one_event = cls(event)
            one_event.creator = user.User(data)
            results.append(one_event) 
        return events
    
    
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE events.id = %(id)s;"
        result = connectToMySQL("group_project_schema").query_db(query,data)
        result = result[0]
        event = cls(result)
        event.user = user.User(
                {
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "pwd" : result["pwd"],
                    "created_at": result["created_at"],
                    "updated_at": result["updated_at"]
                }
            )
        return event
    
    @classmethod
    def get_by_event_type(cls, data):
        query = "SELECT * FROM events WHERE event_type = %(event_type)s;"
        results = connectToMySQL('group_project_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL('group_project_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_event(cls, form_data):
        query = "UPDATE events SET event_type=%(event_type)s, location=%(location)s, spots_open=%(spots_open)s, event_date=%(event_date)s, event_time=%(event_time)s WHERE id=%(id)s;"
        return connectToMySQL('group_project_schema').query_db(query, form_data)
    
    @classmethod
    def delete_event(cls, data):
        
        one_event = cls.get_one(data)
        if session['user_id'] != one_event.user_id:
            session.clear()
            return redirect('/')
        
        query = "DELETE FROM events WHERE id=%(id)s;"
        return connectToMySQL('group_project_schema').query_db(query, data)
    
   
        
    
    @staticmethod
    def event_validator(data):
        
        is_valid = True
        
        if len(data["event_type"]) == 0:
            is_valid = False
            flash("Event type is required.")
        if len(data["location"]) < 3:
            is_valid = False
            flash("Location must be at least 3 characters.")
        if data['spots_open'] == '':
            is_valid = False
            flash("Number of spots open is required.")
        elif int(data['spots_open']) < 1:
            flash("Must be min 1 spot open.")
            is_valid = False
        if data['event_date'] == '':
            is_valid = False
            flash("Date of event is required.")
        if data['event_time'] == '':
            is_valid = False
            flash("Time of event is required.")
            
        return is_valid
    
   