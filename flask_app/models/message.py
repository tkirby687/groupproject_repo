from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, redirect
from flask_app.models import user
from flask_app.models import event
from flask_app.models import message


class Message:
    def __init__(self, data):
        self.id = data['id']
        self.event_message = data['event_message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.event_id = data['event_id']
        self.user_messages = []
        self.event_messages = []
        self.creator = None
        
        # Class method to Create
    @classmethod
    def create_message(cls, form_data):
        query = "INSERT INTO messages (event_message,  event_id, user_id) VALUES ( %(event_message)s,  %(event_id)s,  %(user_id)s);"
        return connectToMySQL('group_project_schema').query_db(query, form_data)
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM messages WHERE event_id = %(event_id)s;"
        results = connectToMySQL("group_project_schema").query_db(query,data)
        return results
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM events LEFT JOIN messages ON events.id = messages.event_id LEFT JOIN users ON users.id = messages.user_id WHERE events.id = %(id)s;"
        results = connectToMySQL('group_project_schema').query_db(query,data)
                
        event = cls(results[0])        
        for row in results:
                        
            if row['users.id'] == None:
                break
           
            data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "pwd": row['pwd'],
                "event_message" : row['event_message'],
                "event_type" : row['event_type'],
                "event_id" : row['event_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            event.user_messages.append(user.User(data))
        return event
    
    