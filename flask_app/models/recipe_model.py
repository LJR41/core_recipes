# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_app.models import user_model

DATE_REGEX = re.compile("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$")

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_thirty = data['under_thirty']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def new_recipe(cls,data):
        query = """
            INSERT INTO recipes (name,description,instruction,under_thirty,date,user_id)
            VALUES (%(name)s,%(description)s,%(instruction)s,%(under_thirty)s,%(date)s,%(user_id)s)
            """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all_recipes(cls):
        query= """
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id
            """
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        if results:
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.cook = this_user
                all_recipes.append(this_recipe)
        return all_recipes
    
    @classmethod
    def get_one_recipe(cls,data):
        query= """
            SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id
            WHERE recipes.id = %(id)s
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            this_recipe = cls(results[0])
            user_data = {
                    **results[0],
                    'id' : results[0]['users.id'],
                    'created_at' : results[0]['users.created_at'],
                    'updated_at' : results[0]['users.updated_at']
                }
            this_user = user_model.User(user_data)
            this_recipe.cook = this_user
            return this_recipe
        return False

    @classmethod
    def delete_recipe(cls,data):
        query ="""
            DELETE FROM recipes WHERE id = %(id)s
            """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def edit_recipe(cls,data):
        query = """
            UPDATE recipes
            SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under_thirty = %(under_thirty)s, date = %(date)s
            WHERE id = %(id)s
            """
        return connectToMySQL(DATABASE).query_db(query,data)

    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 1:
            flash('Please enter a name for this recipe', 'rec')
            is_valid= False
        elif len(data['name']) < 3:
            flash('Name must 3 characters or more', 'rec')
            is_valid = False
        if len(data['description']) < 1:
            flash('Please enter a description for this recipe', 'rec')
            is_valid= False
        elif len(data['description']) < 3:
            flash('Description must 3 characters or more', 'rec')
            is_valid = False
        if len(data['instruction']) < 1:
            flash('Please enter instructions for this recipe', 'rec')
            is_valid= False
        elif len(data['instruction']) < 3:
            flash('Instructions must 3 characters or more', 'rec')
            is_valid = False
        if 'under_thirty' not in data:
            flash('Please select if the recipe takes under thirty minutes to prepare', 'rec')
            is_valid = False
        if 'date' not in data:
            flash('Please select a date for when this recipe was made')
        return is_valid