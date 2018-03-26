from flask import Flask, render_template, redirect, session, flash, request

from mysqlconnection import MySQLConnector


app = Flask(__name__)
#secret_key = 'ThisIsMysecretkey1'
app.secret_key = "ThisIsMysecretkey2"

import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

mysql = MySQLConnector(app, 'emaildb')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
	email = request.form['email']
	print email

	if not EMAIL_REGEX.match(email):
		flash('Please enter a valid email.')
		print "Email fail"
		return redirect('/')
	else:
		query = "INSERT INTO email(email, created_at) VALUES(:email, NOW())"
		data = {
			'email' : request.form['email']
		}
		session['email'] = email
		mysql.query_db(query, data)
		return redirect('/success')
@app.route('/success')
def success():
    query = "SELECT * FROM email"                           # define your query
    emails = mysql.query_db(query)                           # run query with query_db()
    return render_template('success.html', all_emails=emails, email=session['email']) # pass data to our template

@app.route('/home')
def home():
    	session.pop('email')
	return redirect('/')

@app.route('/remove_email/<email_id>')
def delete(email_id):
    query = "DELETE FROM email WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)
