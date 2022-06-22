from datetime import datetime, timedelta
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
    if len(request.form['last_name']) < 1:
        is_valid = False
        dict_of_errors['last_name'] = "Please enter a last name"
    if len(request.form['password']) < 1:
        is_valid = False
        dict_of_errors['password'] = "Please enter a password"
    if len(request.form['password']) > 1 and len(request.form['password']) < 8:
        is_valid = False
        dict_of_errors['password'] = "password should be 8 characters minimum"
    if request.form['password'] != request.form['cpassword']:
        is_valid = False
        dict_of_errors['cpassword'] = "password mismatch"
    if len(request.form['email']) < 1:
        is_valid = False
        dict_of_errors['email'] = "Please enter an email"
    
    
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        if 'email' not in dict_of_errors.keys():
            dict_of_errors['email'] = "Invalid email address!"
    
    if not is_valid:
        flash(dict_of_errors, "register") 
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    mysql = connectToMySQL("mydb")
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
    if len(request.form['password']) < 1:
        is_valid = False
        dict_of_errors['password'] = "Please enter a last name"

    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        if 'email' not in dict_of_errors.keys():
            dict_of_errors['email'] = "Invalid email address!"

    if not is_valid:
        flash(dict_of_errors, "login")
        return redirect("/")
    mysql = connectToMySQL("mydb")
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


def get_user():
    mysql = connectToMySQL("mydb")
    cuser_query = "SELECT * FROM users WHERE id = %(id)s;"
    cuser_data = { "id" : session['userid'] }
    return mysql.query_db(cuser_query, cuser_data)[0]
    

def get_all_users():
    mysql = connectToMySQL("mydb")
    query = "SELECT * FROM users WHERE id != %(id)s;"
    data = { "id" : session['userid'] }
    return mysql.query_db(query, data)

def get_all_recieved_messages():
    mysql = connectToMySQL("mydb")
    query = "SELECT * FROM users JOIN messages ON users.id = messages.sender_id WHERE recipient_id = %(id)s ORDER BY messages.created_at DESC;"
    data = { "id" : session['userid'] }
    return mysql.query_db(query, data)

def get_all_sent_messages():
    mysql = connectToMySQL("mydb")
    query = "SELECT * FROM users JOIN messages ON users.id = messages.sender_id where messages.sender_id = %(id)s;"
    data = { "id" : session['userid'] }
    return mysql.query_db(query, data)

def datetimecompare(value, format = '%H'):
    # print(datetime.now() - value)
    result = datetime.now() - value
    print(result)
    hours, remainder = divmod(result.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    # return f'{int(hours)}:{int(minutes)}'
    # Formatted only for hours and minutes
    return f'{int(hours)}'

# adding custom filter to be accessed from jinja template
app.jinja_env.filters['datetimecompare'] = datetimecompare

@app.route("/success")
def welcome():
    result = get_all_users()
    cuser = get_user()
    all_recieved_messages = get_all_recieved_messages()
    all_sent_messages = get_all_sent_messages()

    print(all_recieved_messages)
    flash("you have successfully logged in!")
    return render_template("welcome.html", all_users = result, current_user=cuser, all_recieved_messages = all_recieved_messages, all_sent_messages = all_sent_messages)

def create_message(content, recipient_id):
    mysql = connectToMySQL("mydb")
    query = "INSERT INTO messages (content, sender_id, recipient_id) VALUES(%(content)s, %(sender_id)s, %(recipient_id)s); "
    data = { "content":content, "sender_id" : session['userid'], "recipient_id":recipient_id}
    return mysql.query_db(query, data)

def get_message(id):
    mysql = connectToMySQL("mydb")
    cuser_query = "SELECT * FROM messages WHERE id = %(id)s;"
    cuser_data = { "id" : id }
    return mysql.query_db(cuser_query, cuser_data)[0]

@app.route("/sendmessage/<int:recipient_id>", methods=["POST"])
def send_message(recipient_id):
    create_message(request.form["message"], recipient_id)
    return redirect("/success")

@app.route("/deletemessage/<int:id>")
def delete_message(id):
    print(get_message(id))
    if get_message(id)['sender_id'] != session['userid']:
        session['messageId'] = id
        return redirect("/danger")
    mysql = connectToMySQL("mydb")
    cuser_query = "DELETE FROM messages WHERE id = %(id)s;"
    cuser_data = { "id" : id }
    mysql.query_db(cuser_query, cuser_data)
    flash("you have deleted message successfully!")
    return redirect("/success")

@app.route("/danger")
def danger():
    return render_template("danger.html", his_ip= request.remote_addr )

@app.route("/logout")
def logout():
    session.clear()
    flash("you have successfully logged out!")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)