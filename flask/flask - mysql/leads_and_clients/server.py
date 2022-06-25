from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL      # import the function that will return an instance of a connection
import json
app = Flask(__name__)
app.secret_key = '123*asdhkjahskdjhaASJHDK'



def get_all_customers_leads(as_customer_name = "customer_name" ,as_leads = "y"):
    mysql = connectToMySQL("lead_gen_business")
    query = f"""
        SELECT concat(clients.first_name, " ",clients.last_name ) as {as_customer_name}, count(leads.leads_id) as {as_leads} FROM clients 
        JOIN sites ON clients.client_id = sites.client_id
        JOIN leads ON sites.site_id = leads.site_id group by clients.client_id ORDER BY {as_leads} DESC
    """
    return mysql.query_db(query)

def get_all_customers_leads_for_period(start_date, end_date, as_customer_name = "customer_name" , as_leads = "y"):
    mysql = connectToMySQL("lead_gen_business")
    query = f"""
        SELECT concat(clients.first_name, " ",clients.last_name ) as "{as_customer_name}", count(leads.leads_id) as "{as_leads}" FROM clients 
        JOIN sites ON clients.client_id = sites.client_id
        JOIN leads ON sites.site_id = leads.site_id WHERE leads.registered_datetime > "{start_date}" AND leads.registered_datetime < "{end_date}" group by clients.client_id ORDER BY "{as_leads}" DESC
    """
    return mysql.query_db(query)

@app.route("/")
def index():
    all_customers = get_all_customers_leads()
    flash("you have successfully logged in!")
    # data = get_all_customers_leads()
    # print(data)
    return render_template("index.html", all_customers = all_customers, )

@app.route("/betweendates", methods=['POST'])
def between_dates():
    all_customers = get_all_customers_leads_for_period(request.form['start_date'], request.form['end_date'])
    print(all_customers)
    session['all_customers'] = all_customers
    # session['data'] = get_all_customers_leads_for_period(request.form['start_date'], request.form['end_date'], 'label','y')
    return redirect("/leads-dates")

@app.route("/leads-dates")
def leads_with_dates():
    flash("you have successfully logged in!")
    return render_template("index.html", all_customers = session['all_customers'], data = session['data'])


if __name__ == "__main__":
    app.run(debug=True)