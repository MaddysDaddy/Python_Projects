from flask import Flask, session, render_template, flash, request, redirect

from mysqlconnection import MySQLConnector

from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

mysql = MySQLConnector(app, 'login_db')

app.secret_key = "MySecretKey1"

import re
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


@app.route('/')
def index():
    if 'user' not in session:
        return render_template('index.html')
    else:
        return redirect('/main')


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['confirm-password']
    errors = []

    if len(first_name) < 2:
        errors.append('First name must be at least 2 characters long.')

    if not NAME_REGEX.match(first_name):
        errors.append('First name must be letters only.')

    if len(last_name) < 2:
        errors.append('Last name must be longer than 2 characters')

    if not NAME_REGEX.match(last_name):
        errors.append('Last name must be letters only.')

    if not EMAIL_REGEX.match(email):
        errors.append('Please enter a valid email address.')

    if len(password) < 8:
        errors.append(
            'Password that is at least 8 characters long')

    if password != cpassword:
        errors.append('Passwords do not match')

    if len(errors) > 0:
        for error in errors:
            flash(error, 'regerror')

    else:
        pw_hash = bcrypt.generate_password_hash(password)
        query = "INSERT INTO users(first_name, last_name, email, pw_hash, created_at, updated_at) VALUES(:first_name, :last_name, :email, :pw_hash, NOW(), NOW())"
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'pw_hash': pw_hash
        }

        user = mysql.query_db(query, data)
        get_user_query = "SELECT * FROM users WHERE id = :id"
        user_data = {
            'id': user
        }
        new_user = mysql.query_db(get_user_query, user_data)
        session['user'] = new_user
        return redirect('/main')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM users WHERE email = :email"
    data = {
        'email': email
    }
    try:
        user = mysql.query_db(query, data)

        if bcrypt.check_password_hash(user[0]['pw_hash'], password):
            session['user'] = user
            return redirect('/main')
        else:
            print "Incorrect login info."
            flash('Incorrect login info.', 'error')
            return redirect('/')

    except IndexError:
        user = 'null'
        flash('Username not found. Please register below.', 'error')
        return redirect('/')


@app.route('/main')
def main():
    first_name = session['user'][0]['first_name']
    last_name = session['user'][0]['last_name']
    full_name = first_name + " " + last_name
    return render_template('main.html', user=first_name, fullname=full_name)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


app.run(debug=True)
