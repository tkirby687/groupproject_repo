from operator import truediv
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# modeling the class after the users table
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pwd = data['pwd']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    # Class method to Create user
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , pwd ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(pwd)s );"
        result  = connectToMySQL('group_project_schema').query_db( query, data )
        return result
    
    # Class method to Retrieve (all)
    @classmethod
    def get_all(cls):        
        query = "SELECT * FROM users;"
        results = connectToMySQL('group_project_schema').query_db(query)
        users = []        
        for user in results:
            users.append( cls(user) )
        return users
    
    # Class method to Retrieve user by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('group_project_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        
        query  = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL('group_project_schema').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update_info(cls, form_data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, pwd=%(pwd)s  WHERE id=%(id)s;"
        return connectToMySQL('group_project_schema').query_db(query, form_data)
    
    # Static method to validate user registration
    @staticmethod
    def user_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('group_project_schema').query_db(query, user)
        if len(result) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user["first_name"]) < 2:
            is_valid = False
            flash("First name must be at least 2 characters.", "register")
        if len(user["last_name"]) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.", "register")
        if len(user["pwd"]) < 8:
            is_valid = False
            flash("Password is required and must be at least 8 characters.", "register")
        if user['pwd'] != user['confirm_pwd']:
            flash("Passwords do not match!", "register")
        return is_valid