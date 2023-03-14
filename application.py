from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'customer'

mysql = MySQL(app)
app.secret_key = 'llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        details = request.form
        username = details['username']
        password = details['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM customer WHERE username = %s and password = %s", (username, password))
            records = cur.fetchall()
            if cur.rowcount == 0:
                return render_template('login.html') # add variable for indicating wrong username/password
            else:
                return render_template('index.html') # add variable for showing username
        except Exception as e:
            return "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        details = request.form
        username = details['username']
        password = details['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM customer WHERE binary username = %s", (username))
            records = cur.fetchall()
            if cur.rowcount != 0:
                return render_template('register.html') # add variable for indicating username is in use
            else:
                cur.execute("INSERT INTO customer VALUES (...)") # TODO add variables in the right order    
                return render_template('index.html') # add variable for showing username
        except Exception as e:
            "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

    return render_template('register.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)