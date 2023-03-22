from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'voyagevault'

mysql = MySQL(app)
app.secret_key = 'llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE email = %s', (email,))
        user_exists = cursor.fetchone()
        cursor.close()
        if user_exists:
            if check_password_hash(user_exists['password'], password):
                session['loggedin'] = True
                session['cID'] = user_exists['cID']
                session['fname'] = user_exists['fname']
                session['lname'] = user_exists['lname']
                session['email'] = user_exists['email']
                session['hpnum'] = user_exists['hpnum']
                return redirect(url_for('index'))
            else:
                flash('Incorrect password!',category='error')
        else:
            flash('Incorrect email!',category='error')

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form \
        and 'password' in request.form and 'email' in request.form and 'hpnum' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        hpnum = request.form['hpnum']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!',category='error')
        elif not re.match(r'[A-Za-z0-9]+', fname) or not re.match(r'[A-Za-z0-9]+', lname):
            flash('Invalid name!', category='error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!',category='error')
        else:
            cursor.execute('INSERT INTO customer VALUES (NULL, %s, %s, %s, %s, %s)', (fname, lname, email, hpnum, generate_password_hash(password),))
            mysql.connection.commit()
            flash('Congratulations, you have successfully registered. Try logging in now!', category='success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)