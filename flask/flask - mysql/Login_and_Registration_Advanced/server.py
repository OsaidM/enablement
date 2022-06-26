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
            "email": request.form['email'],
            "user_level" : 1}
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

def get_all_users():
    mysql = connectToMySQL("user_schema")
    query = "SELECT * FROM users"
    return mysql.query_db(query)

@app.route("/success")
def welcome():
    mysql = connectToMySQL("user_schema")
    query = "SELECT * FROM users WHERE id = %(id)s;"
    if 'userid' not in session.keys():
        flash("you are not logged in!")
        return redirect("/danger")
    data = { "id" : session['userid'] }
    result = mysql.query_db(query, data)
    all_users = get_all_users()
    if result[0]['user_level'] == 9:
        flash("you have successfully logged in!")
        return render_template("welcome_admin.html", result = result[0], all_users = all_users)
    if result[0]['user_level'] == 1:
        flash("you have successfully logged in!")
        return render_template("welcome_user.html", result = result[0])
    flash("error occured while logging in", "logout")
    return redirect("/")

@app.route("/danger")
def danger():
    return render_template("danger.html", his_ip= request.remote_addr )

def check_if_secure():
    if not 'userid' in session.keys():# if he is logged in
        session.clear()
        flash("sorry you are not logged in", 'logout')
        return False

    mysql = connectToMySQL("user_schema")
    query = f"SELECT * FROM users WHERE id = {session['userid']}"
    result = mysql.query_db(query)
    print("result ", result)
    print("id ", session['userid'])
    if session['userid'] != result[0]['id']:# if he is the same user
        session.clear()
        flash("are you trying to hack?", 'logout')
        return False
    if result[0]['user_level'] != 9:# if he is an admin
        session.clear()
        flash("are you trying to hack?", 'logout')
        return False
    return True


@app.route("/remove-user/<id>")
def remove_user(id):
    if check_if_secure():
        mysql = connectToMySQL("user_schema")
        query = f"DELETE FROM users WHERE id = {id};"
        mysql.query_db(query)
        return redirect("/success")
    return redirect("/")

@app.route("/remove-admin-access/<id>")
def remove_admin_access(id):
    if check_if_secure():
        mysql = connectToMySQL("user_schema")
        query = f"UPDATE users SET user_level=1 WHERE id = {id};"
        mysql.query_db(query)
        return redirect("/success")
    return redirect("/")

@app.route("/make-admin/<id>")
def make_admin(id):
    if check_if_secure():
        mysql = connectToMySQL("user_schema")
        query = f"UPDATE users SET user_level=9 WHERE id = {id};"
        mysql.query_db(query)
        return redirect("/success")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    flash("you have successfully logged out!", 'logout')
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)