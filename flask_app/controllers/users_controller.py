from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)
from flask_app import DATABASE


# @app.route('/register', methods=['POST'])
# def register():
#     if not User.validate_user(request.form):
#         # we redirect to the template with the form.
#         return redirect('/')
#     # ... do other things
#     return redirect('/dashboard')

@app.route('/')
def go_home():
    if 'user_id' in session:
        return redirect('/recipes')
    return render_template('reg_login.html')

@app.route('/user/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect ('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' :hashed_pass,
        'cpass' : hashed_pass
    }
    logged_user_id = User.create_user(data)
    session['user_id'] = logged_user_id
    return redirect('/recipes')

@app.route('/user/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    potential_user = User.get_by_email(data)
    if not potential_user:
        flash("Invalid Credentials", 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash ('Invalid Credentials', 'log')
        return redirect('/')
    session['user_id'] = potential_user.id
    return redirect('/recipes')

@app.route('/user/logout')
def logout():
    del session['user_id']
    return redirect('/')
