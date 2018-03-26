from flask import Flask, session, render_template, flash, request, redirect

from mysqlconnection import MySQLConnector

from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

mysql = MySQLConnector(app, 'wall_db')

app.secret_key = "MySecretKey1"
import time
import re
import datetime

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


@app.route('/')
def index():
    if 'user' not in session:
        return render_template('index.html')
    else:
        return redirect('/wall')


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
        return redirect('/wall')
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
            return redirect('/wall')
        else:
            print "Incorrect login info."
            flash('Incorrect login info.', 'error')
            return redirect('/')

    except IndexError:
        user = 'null'
        flash('Username not found. Please register below.', 'error')
        return redirect('/')


@app.route('/wall')
def main():
    first_name = session['user'][0]['first_name']
    last_name = session['user'][0]['last_name']
    full_name = first_name + " " + last_name
    userid = session['user'][0]['id']

    current_time = datetime.datetime.now()
    current_minus_30 = datetime.datetime.now() - datetime.timedelta(minutes=30)

    query = 'SELECT m.id, u.id AS user_id, message, CONCAT(first_name, " ",last_name) AS fullname, m.created_at FROM message m INNER JOIN users u on u.id = m.user_id ORDER BY created_at DESC'

    posts = mysql.query_db(query)

    comments_query = 'SELECT c.commenter_id, c.message_id, c.comment, CONCAT(u.first_name," ", u.last_name) as fullname, c.created_at FROM comment c INNER JOIN users u on u.id = c.commenter_id'
    comments = mysql.query_db(comments_query)

    return render_template('main.html', user=first_name, fullname=full_name, posts=posts, user_id=userid, comments=comments, timelimit=current_minus_30)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


@app.route('/message', methods=['POST'])
def message():
    message = request.form['message']
    user = session['user'][0]['id']

    if len(message) > 0:
        query = "INSERT INTO message(user_id, message, created_at, updated_at) VALUES(:user_id, :message, now(), now())"
        data = {
            'user_id': user,
            'message': message
        }
        mysql.query_db(query, data)
        return redirect('/wall')
    else:
        flash('Message cannot be empty.', 'messerror')
        return redirect('/wall')


@app.route('/comment/<post_id>', methods=['POST'])
def comment(post_id):

    comment = request.form['comment']

    if len(comment) < 1:
        flash("Comment can't be blank", 'commenterror')
        return redirect('/wall')
    else:
        query = "INSERT INTO comment(commenter_id, message_id, comment, created_at, updated_at) VALUES(:commenter_id, :message_id, :comment, now(), now())"
        data = {
            'commenter_id': session['user'][0]['id'],
            'message_id': post_id,
            'comment': comment
        }
        mysql.query_db(query, data)
        return redirect('/wall')


@app.route('/delete/<post_id>')
def delete_message(post_id):
    # Get current time - 30 minutes
    current_minus_30 = datetime.datetime.now() - datetime.timedelta(minutes=30)

    # Grab all information about the post
    query = 'SELECT * FROM message WHERE id = :post_id'
    data = {
        'post_id': post_id
    }

    post = mysql.query_db(query, data)
    print post[0]['created_at']
    print current_minus_30

    # Make sure the logged in user is the one who made the post
    if session['user'][0]['id'] == post[0]['user_id']:
        if post[0]['created_at'] > current_minus_30:
            # Delete all comments from post
            delete_c_query = 'DELETE FROM comment WHERE message_id = :post_id'
            delete_c_data = {
                'post_id': post_id
            }
            mysql.query_db(delete_c_query, delete_c_data)

            # Delete the post
            delete_m_query = 'DELETE FROM message WHERE id = :post_id'
            delete_m_data = {
                'post_id': post_id
            }
            mysql.query_db(delete_m_query, delete_m_data)

            return redirect('/wall')
        else:
            flash(
                'Doh! Posts can only be deleted within thirty minutes of creation.', 'deleteError')
            return redirect('/wall')


app.run(debug=True)
