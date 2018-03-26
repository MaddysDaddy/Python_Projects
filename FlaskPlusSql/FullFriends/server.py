from flask import Flask, render_template, redirect, request, session, flash

from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'ThisIsMySecretKey1'

import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

mysql = MySQLConnector(app, 'full_friends_db')


@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)

    return render_template('index.html', all_friends=friends)


@app.route('/friends', methods=['POST'])
def friends():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email = request.form['email']
    errors = []

    if len(first_name) < 1:
        errors.append('Please enter your first name.')
    if len(last_name) < 1:
        errors.append('Please enter a last name.')
    if not EMAIL_REGEX.match(email):
        errors.append('Please enter a valid email.')

    if len(errors) > 0:
        for error in errors:
            flash(error)
    else:
        query = "INSERT INTO friends(first_name, last_name, email, created_at, last_updated) VALUES(:first_name, :last_name, :email, NOW(), NOW())"
        data = {
            'first_name': request.form['fname'],
            'last_name': request.form['lname'],
            'email': request.form['email']
        }

        mysql.query_db(query, data)
        return redirect('/')

    return redirect('/')


@app.route('/friends/<friend_id>/edit', methods=['GET'])
def edit(friend_id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {
        'id': friend_id
    }
    friend = mysql.query_db(query, data)

    print friend
    return render_template('edit.html', friend=friend)


@app.route('/friends/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, last_updated = NOW() WHERE id = :id"
    data = {
        'id': friend_id,
        'first_name': request.form['firstName'],
        'last_name': request.form['lastName'],
        'email': request.form['fEmail']
    }
    mysql.query_db(query, data)
    return redirect('/')


@app.route('/friends/<friend_id>/delete')
def destroy(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {
        'id': friend_id
    }
    mysql.query_db(query, data)
    return redirect('/')


app.run(debug=True)
