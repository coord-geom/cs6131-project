from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random
from datetime import datetime
import sys
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

@app.route('/search', methods=['GET','POST'])
@app.route('/search/tag/<tagname>', methods=['GET','POST'])
def search(tagname=None):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT MIN(aprice) a, MAX(aprice) b FROM package')
        cost = cursor.fetchone() 
        mincost = cost['a']
        maxcost = cost['b']
        cursor.execute('SELECT * FROM package')
        fields = ['package name','location','tags','agency']
        if not tagname == None:
            query = 'SELECT distinct p.* FROM package p, ptag t WHERE p.pid=t.pid and tag like %s'
            cursor.execute(query, (tagname,))
            packages = cursor.fetchall()
            cursor.execute('SELECT * FROM ptag')
            ptag = cursor.fetchall()
            cursor.close()
            return render_template('search.html',packages=packages, ptag=ptag, fields=fields, maxcost=maxcost, mincost=mincost)
        
        elif request.method == 'POST':
            category = request.form.get('category')
            if category in fields:
                search1 = request.form['query']
                search = '%' + search1 + '%'
                date = request.form['depdate']
                rating = request.form['rating']
                cap = request.form['cap']
                cost = request.form['cost']
                query = 'SELECT distinct p.* FROM package p, tourgroup g '
                query2 = " and departure >= %s and (p.pid=g.pid or p.pid not in (SELECT pid FROM tourgroup)) and cursize+%s <= maxsize and prating >= %s and aprice <= %s"
                if category == fields[0]:
                    query += 'WHERE pname like %s'
                    query += query2
                    cursor.execute(query, (search,date,cap,rating,cost,))
                elif category == fields[1]:
                    query += ', location l, visit v, country c WHERE (lname like %s or region like %s or cname like %s) and v.pid=p.pid and v.lid=l.lid and l.countryid = c.countryid'
                    query += query2
                    cursor.execute(query, (search,search,search,date,cap,rating,cost,))
                elif category == fields[2]:
                    query += ', ptag t WHERE p.pid=t.pid and tag like %s'
                    query += query2
                    cursor.execute(query, (search,date,cap,rating,cost,))
                elif category == fields[3]:
                    query += ', agency a WHERE p.aid=a.aid and aname like %s'
                    query += query2
                    cursor.execute(query, (search,date,cap,rating,cost,))
                packages = cursor.fetchall()
                cursor.execute('SELECT * FROM ptag')
                ptag = cursor.fetchall()
                cursor.close()
                return render_template('search.html',packages=packages, ptag=ptag, fields=fields, search=search1, maxcost=maxcost, mincost=mincost)
        else:
            packages = cursor.fetchall() #fetch all records
            cursor.execute('SELECT * FROM ptag')
            ptag = cursor.fetchall()
            cursor.close()
            return render_template('search.html',packages=packages, ptag=ptag, fields=fields, maxcost=maxcost, mincost=mincost)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html')
    return redirect(url_for('login'))

@app.route('/package/<pid>',methods=['GET','POST'])
def view_package(pid):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if pid == '0':
            cursor.execute('SELECT pid FROM package')
            pids = cursor.fetchall()
            return redirect(url_for('view_package',pid=random.choice(pids)['pid']))
        elif request.method == 'GET':
            cursor.execute('SELECT p.*, aname FROM package p, agency a WHERE pid = %s and p.aid=a.aid',(str(pid),))
            package = cursor.fetchone()
            cursor.execute('SELECT r.*, concat(fname,\' \',lname) cname FROM review r, customer c WHERE pid = %s and r.cid = c.cid',(str(pid),))
            reviews = cursor.fetchall()
            cursor.close()
            return render_template('package.html',package=package,reviews=reviews)
        elif request.method == 'POST':
            if 'details' in request.form:
                rating = request.form['rating']
                details = request.form['details']
                cursor.execute('SELECT * FROM review WHERE cid=%s and pid=%s',(str(session['cID']),str(pid),))
                review = cursor.fetchone()
                if review:
                    flash('Sorry, you may only leave one review per package! You may still edit or delete your current review.', category='error')
                    return redirect(url_for('view_package',pid=pid))
                else:
                    cursor.execute('INSERT INTO review VALUES (%s,%s,%s,%s)',(str(session['cID']),str(pid),str(rating),details,))
                    mysql.connection.commit()
                    flash('Thanks for leaving a review!', category='success')
                    return redirect(url_for('view_package',pid=pid))
            elif 'update-review' in request.form:
                rating = request.form['rating']
                details = request.form['update-review']
                cursor.execute('UPDATE review SET rating=%s, content=%s WHERE cid=%s and pid=%s',(str(rating),details,str(session['cID']),str(pid),))
                mysql.connection.commit()
                return redirect(url_for('view_package',pid=pid))
            elif 'delete-review' in request.form:
                cursor.execute('DELETE FROM review WHERE cid=%s and pid=%s',(str(session['cID']),str(pid),))
                mysql.connection.commit()
                return redirect(url_for('view_package',pid=pid))
    else:
        return redirect(url_for('login'))
    
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)