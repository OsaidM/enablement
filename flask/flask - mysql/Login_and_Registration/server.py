
from asyncio.windows_events import NULL
import re	# the regex module
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL      # import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = '123*asdhkjahskdjhaASJHDK'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route("/")
def index():

    return render_template("login.html")

@app.route("/register", methods=['POST'])
def register():
    dict_of_errors = {}
    is_valid = True
    if len(request.form['first_name']) < 1:
        is_valid = False
        dict_of_errors['first_name'] = "Please enter a first name"
        # flash({'first_name':"Please enter a first name"})
    if len(request.form['last_name']) < 1:
        is_valid = False
        dict_of_errors['last_name'] = "Please enter a last name"
        # flash({'last_name':"Please enter a last name"})
    if len(request.form['password']) < 1:
        is_valid = False
        dict_of_errors['password'] = "Please enter a password"
        # flash({'password':"Please enter a password"})
    if len(request.form['password']) > 1 and len(request.form['password']) < 8:
        is_valid = False
        dict_of_errors['password'] = "password should be 8 characters minimum"
        # flash({'password':"password should be 8 characters minimum"})
    if request.form['password'] != request.form['cpassword']:
        is_valid = False
        dict_of_errors['cpassword'] = "password mismatch"
        # flash({'cpassword':"password mismatch"})
    if len(request.form['email']) < 1:
        is_valid = False
        dict_of_errors['email'] = "Please enter an email"
        # flash({'email':"Please enter a email"})
    
    
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        if 'email' not in dict_of_errors.keys():
            dict_of_errors['email'] = "Invalid email address!"
        # flash({'email':"Invalid email address!"})
    
    if not is_valid:
        flash(dict_of_errors, "register") 
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    mysql = connectToMySQL("user_schema")
    query = "INSERT INTO users (first_name, last_name, password, email) VALUES (%(first_name)s, %(last_name)s, %(password)s, %(email)s );"
    # put the pw_hash in our data dictionary, NOT the password the user provided
    data = { 
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "password" : pw_hash,
            "email": request.form['email']}
    is_created = mysql.query_db(query, data)
    if not is_created:
        dict_of_errors['database_error'] = "database error"
        flash(dict_of_errors, "register")
        return redirect("/")
    dict_of_errors['successful'] = "User successfully created!"
    flash(dict_of_errors, "register")
    return redirect("/")

@app.route("/login", methods=['POST'])
def login():
    print(request.form)
    dict_of_errors = {}
    is_valid = True
    if len(request.form['email']) < 1:
        is_valid = False
        dict_of_errors['email'] = "Please enter a first name"
        # flash({'first_name':"Please enter a first name"})
    if len(request.form['password']) < 1:
        is_valid = False
        dict_of_errors['password'] = "Please enter a last name"

    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        if 'email' not in dict_of_errors.keys():
            dict_of_errors['email'] = "Invalid email address!"

    if not is_valid:
        flash(dict_of_errors, "login")
        return redirect("/")
    mysql = connectToMySQL("user_schema")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)

    if result: # if user exists
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['userid'] = result[0]['id']
            return redirect('/success')
    dict_of_errors['login_error'] = "You could not be logged in"
    flash(dict_of_errors, "login")
    return redirect("/")


@app.route("/success")
def welcome():
    mysql = connectToMySQL("user_schema")
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = { "id" : session['userid'] }
    result = mysql.query_db(query, data)
    print(result)
    flash("you have successfully logged in!")
    return render_template("welcome.html", result = result[0])

@app.route("/logout")
def logout():
    session.clear()
    flash("you have successfully logged out!")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)