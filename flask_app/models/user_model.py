# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
from flask import flash

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# class User:
#     @staticmethod
#     def validate_user( user ):
#         is_valid = True
#         # test whether a field matches the pattern
#         if not EMAIL_REGEX.match(user['email']): 
#             flash("Invalid email address!")
#             is_valid = False
#         return is_valid

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query = """
            INSERT INTO users (first_name,last_name,email,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
            """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query= """
            SELECT * FROM users WHERE id = %(id)s
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_email(cls,data):
        query= """
            SELECT * FROM users WHERE email = %(email)s
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash('Please enter a FIRST NAME', 'reg')
            is_valid = False
        elif len(data['first_name']) < 2:
            flash('FIRST NAME must contain more than 2 letters', 'reg')
            is_valid = False
        elif not data['first_name'].isalpha():
            flash('First NAME can only contain letters', 'reg')
        if len(data['last_name']) < 1:
            flash('Please enter a LAST NAME', 'reg')
            is_valid = False
        elif len(data['last_name']) < 2:
            flash('LAST NAME must contain more than 2 letters', 'reg')
            is_valid = False
        elif not data['last_name'].isalpha():
            flash('LAST NAME can only contain letters', 'reg')
        if len(data['email'])< 1:
            flash('Please enter an email address', 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Email must be in proper format', 'reg')
        else:
            potential_user = User.get_by_email({'email': data['email']})
            if potential_user:
                flash('Email is already in database', 'reg')
        if len(data['password']) < 1:
            flash('A password is required', 'reg')
            is_valid = False
        elif len(data['password']) < 8:
            flash('Password must be 8 characters or more', 'reg')
            is_valid=False
        elif data['password'] != data['cpass']:
            flash('Passwords do not match', 'reg')
            is_valid = False
        return is_valid