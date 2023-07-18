from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_app import DATABASE

@app.route('/recipes')
def display_dash():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : session['user_id']
    }
    one_user = User.get_by_id(data)
    all_recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', one_user=one_user, all_recipes=all_recipes)

@app.route('/recipes/new')
def recipe_form():
    if 'user_id' not in session:
        return redirect ('/')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def new_recipe():
    if 'user_id' not in session:
        return redirect ('/recipes')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        **request.form,
        'user_id' : session['user_id']
    }
    Recipe.new_recipe(data)
    return redirect ('/recipes')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    data = {
        'id' : id
    }
    Recipe.delete_recipe(data)
    return redirect ('/recipes')

@app.route('/recipes/<int:id>/view')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect ('/recipes')
    data1 = {
        'id' : id
    }
    data2 = {
        'id' : session['user_id']
    }
    one_user = User.get_by_id(data2)
    one_recipe = Recipe.get_one_recipe(data1)
    return render_template('view.html', one_user=one_user, one_recipe=one_recipe)

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect ('/recipes')
    data = {
        'id' : id
    }
    one_recipe = Recipe.get_one_recipe(data)
    return render_template('edit_recipe.html', one_recipe=one_recipe)

@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    data = {
        **request.form,
        'id' : id
    }
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{id}/edit')
    Recipe.edit_recipe(data)
    return redirect ('/recipes')