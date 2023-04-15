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
    if 'loggedin' in session and 'aID' in session:
        return redirect(url_for('bindex'))
    return render_template('index.html')

@app.route("/b")
def bindex():
    if 'loggedin' in session and 'cID' in session:
        return redirect(url_for('index'))
    return render_template('bindex.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('index'))
    else:
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
    if 'loggedin' in session:
        return redirect(url_for('index'))
    else:
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
   if 'aID' in session:
       return redirect(url_for('bindex'))
   session.clear()
   return redirect(url_for('index'))

@app.route('/b/logout')
def blogout():
    if 'cID' in session:
        return redirect(url_for('index'))
    session.clear()
    return redirect(url_for('bindex'))

@app.route('/b/login',methods=['GET','POST'])
def blogin():
    if 'loggedin' in session:
        return redirect(url_for('bindex'))
    else:
        if request.method == 'POST' and 'aemail' in request.form and 'apassword' in request.form:
            email = request.form['aemail']
            password = request.form['apassword']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM agency WHERE aemail = %s', (email,))
            user_exists = cursor.fetchone()
            cursor.close()
            if user_exists:
                if check_password_hash(user_exists['apassword'], password):
                    session['loggedin'] = True
                    session['aID'] = user_exists['aID']
                    session['aname'] = user_exists['aname']
                    session['email'] = user_exists['aemail']
                    session['hotline'] = user_exists['hotline']
                    return redirect(url_for('bindex'))
                else:
                    flash('Incorrect password!',category='error')
            else:
                flash('Incorrect email!',category='error')

        return render_template('blogin.html')

@app.route('/b/register',methods=['GET','POST'])
def bregister():
    if 'loggedin' in session:
        return redirect(url_for('bindex'))
    else:
        if request.method == 'POST' and 'aname' in request.form \
            and 'apassword' in request.form and 'aemail' in request.form and 'hotline' in request.form:
            aname = request.form['aname']
            password = request.form['apassword']
            email = request.form['aemail']
            hotline = request.form['hotline']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM agency WHERE aemail = %s', (email,))
            account = cursor.fetchone()
            if account:
                flash('Account already exists!',category='error')
            elif not re.match(r'[A-Za-z0-9]+', aname):
                flash('Invalid name!', category='error')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!',category='error')
            else:
                cursor.execute('INSERT INTO agency VALUES (NULL, %s, %s, %s, %s)', (aname, hotline, email, generate_password_hash(password),))
                mysql.connection.commit()
                flash('Congratulations, you have successfully registered. Try logging in now!', category='success')
                return redirect(url_for('blogin'))

        return render_template('bregister.html')

@app.route('/search', methods=['GET','POST'])
@app.route('/search/tag/<tagname>', methods=['GET','POST'])
def search(tagname=None):
    if 'loggedin' in session and 'aID' in session:
        return redirect(url_for('bsearch'))
    elif 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT MIN(aprice) a, MAX(aprice) b FROM package')
        cost = cursor.fetchone() 
        mincost = cost['a']
        maxcost = cost['b']
        cursor.execute('SELECT * FROM package')
        fields = ['package name','location','tags','agency']

        if request.method == 'POST':
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
        elif not tagname == None:
            query = 'SELECT distinct p.* FROM package p, ptag t WHERE p.pid=t.pid and tag like %s'
            cursor.execute(query, (tagname,))
            packages = cursor.fetchall()
            cursor.execute('SELECT * FROM ptag')
            ptag = cursor.fetchall()
            cursor.close()
            return render_template('search.html',packages=packages, ptag=ptag, fields=fields, maxcost=maxcost, mincost=mincost)
        else:
            packages = cursor.fetchall() #fetch all records
            cursor.execute('SELECT * FROM ptag')
            ptag = cursor.fetchall()
            cursor.close()
            return render_template('search.html',packages=packages, ptag=ptag, fields=fields, maxcost=maxcost, mincost=mincost)
    return redirect(url_for('login'))

@app.route('/profile',methods=['GET','POST'])
def profile():
    if 'loggedin' in session:
        if 'cID' in session:
            return render_template('profile.html')
        elif 'aID' in session:
            if request.method == 'POST':
                password = request.form['password']
                email = request.form['email']
                hpnum = request.form['hpnum']

                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address! Updates not done.',category='error')
                else:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE customer set email=%s, password=%s, hpnum=%s WHERE id = %s ', (email, generate_password_hash(password), hpnum, session['cID'],))
                    mysql.connection.commit() #note that you need to commit the changes for INSERT,UPDATE and DELETE statements
                    cursor.close()
                    flash('You have updated your email, contact number and password successfully',category='success')
            elif request.method == 'GET':
                return redirect(url_for('bprofile'))
    return redirect(url_for('login'))

@app.route('/package/<pid>',methods=['GET','POST'])
def view_package(pid):
    if 'loggedin' in session and 'cID' in session:
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

@app.route('/reviews', methods=['GET','POST'])
def review():
    if 'loggedin' in session and 'cID' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'GET':
            cursor.execute('SELECT r.*, concat(fname,\' \',lname) cname, pname FROM review r, customer c, package p WHERE r.cID=%s and r.cID=c.cID and r.pID=p.pID',(session['cID'],))
            reviews = cursor.fetchall()
            return render_template('reviews.html',review=reviews)
        elif request.method == 'POST':
            id = str(request.form['ID'])
            pid = str(request.form['pID'])
            if 'update-review'+id in request.form:
                rating = str(request.form['rating'+id])
                details = request.form['update-review'+id]
                cursor.execute('UPDATE review SET rating=%s, content=%s WHERE cid=%s and pid=%s',(rating,details,str(session['cID']),pid,))
                mysql.connection.commit()
                return redirect(url_for('review'))
            elif 'delete-review'+id in request.form:
                cursor.execute('DELETE FROM review WHERE cid=%s and pid=%s',(str(session['cID']),pid,))
                mysql.connection.commit()
                return redirect(url_for('review'))
    else:
        return redirect(url_for('login'))

@app.route('/b/new/package',methods=['GET','POST'])
def bmake_package():
    if 'loggedin' in session and 'cID' in session:
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM country')
        countries = cursor.fetchall()
        cursor.execute('SELECT distinct tag FROM ptag ORDER BY tag')
        tags = cursor.fetchall()
        cursor.execute('SELECT distinct region FROM location')
        regions = cursor.fetchall()
        cursor.execute('SELECT distinct lname FROM location')
        locations = cursor.fetchall()
        return render_template('bmakePackage.html',countries=countries, tags=tags, locations=locations, regions=regions)
    elif request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        imglink = request.form['imglink']
        ptype = request.form['type']
        pname = request.form['pname']
        desc = request.form['description']
        iti = request.form['itinerary']
        duration = request.form['duration']
        aprice = request.form['aprice']
        cprice = request.form['cprice']
        capacity = request.form['cap']
        link = request.form['link']

        countries = request.form['countryInputs'].split(';')
        locations = request.form['locationInputs'].split(';')
        tags = request.form['tagInputs'].split(';')
        dates = request.form['dates'].split(',')

        cursor.execute('INSERT INTO package (pid,aid,pname,description,duration,aprice,cprice,link,itinerary,tourtype,imagelink) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(session['aID'],pname,desc,duration,aprice,cprice,link,iti,ptype,imglink,))
        cursor.connection.commit()

        cursor.execute('SELECT pID FROM package WHERE aid=%s and pname=%s and description=%s and duration=%s and aprice=%s and cprice=%s and link=%s and itinerary=%s and tourtype=%s and imagelink=%s',(session['aID'],pname,desc,duration,aprice,cprice,link,iti,ptype,imglink,))
        pid = cursor.fetchone()['pID']


        for country in countries:
            if country == '':
                break
            cursor.execute('SELECT countryID FROM country WHERE cname=%s',(country,))
            cid = cursor.fetchone()['countryID']
            cursor.execute('SELECT * FROM packageDest WHERE pid=%s and countryid=%s',(pid,cid,))
            any = cursor.fetchall()
            if not any:
                cursor.execute('INSERT INTO packageDest VALUES (%s,%s)',(pid,cid,))
                cursor.connection.commit()
        
        for tag in tags:
            if tag == '':
                break
            cursor.execute('SELECT * FROM ptag WHERE pid=%s and tag=%s',(pid,tag,))
            any = cursor.fetchall()
            if not any:
                cursor.execute('INSERT INTO ptag VALUES (%s,%s)',(pid,tag,))
                cursor.connection.commit()

        for location in locations:
            if location == '':
                break
            lname, region, cname = location.split('#')
            cursor.execute('SELECT countryID FROM country WHERE cname=%s',(cname,))
            cid = cursor.fetchone()['countryID']
            cursor.execute('SELECT * FROM location WHERE lname=%s and region=%s and countryid=%s',(lname,region,cid,))
            any = cursor.fetchall()
            if not any:
                cursor.execute('INSERT INTO location VALUES (NULL,%s,%s,%s)',(lname,region,cid,))
                cursor.connection.commit()
            cursor.execute('SELECT lID FROM location WHERE lname=%s and region=%s and countryid=%s',(lname,region,cid,))
            lid = cursor.fetchone()['lID']
            if ptype == 'GRP':
                cursor.execute('SELECT * FROM visit WHERE pid=%s and lid=%s',(pid,lid,))
                any = cursor.fetchall()
                if not any:
                    cursor.execute('INSERT INTO visit VALUES (%s,%s)',(pid,lid,))
                    cursor.connection.commit()
            elif ptype == 'FNE':
                cursor.execute('SELECT * FROM recommend WHERE pid=%s and lid=%s',(pid,lid,))
                any = cursor.fetchall()
                if not any:
                    cursor.execute('INSERT INTO recommend VALUES (%s,%s)',(pid,lid,))
                    cursor.connection.commit()
        
        if ptype == 'GRP':
            for date in dates:
                cursor.execute('INSERT INTO tourgroup VALUES (%s,%s,0,%s)',(pid,capacity,date,))
                cursor.connection.commit()

        cursor.close()
        return redirect(url_for('bview_package',pid=pid))
    
@app.route('/b/package/<pid>')
def bview_package(pid):
    if 'loggedin' in session and 'cID' in session:
        return redirect(url_for('index'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        cursor.execute('SELECT p.*, aname FROM package p, agency a WHERE pid = %s and p.aid=a.aid',(str(pid),))
        package = cursor.fetchone()
        cursor.execute('SELECT r.*, concat(fname,\' \',lname) cname FROM review r, customer c WHERE pid = %s and r.cid = c.cid',(str(pid),))
        reviews = cursor.fetchall()
        cursor.close()
        return render_template('bpackage.html',package=package,reviews=reviews)

@app.route('/b/manage')
def bmanage():
    if 'loggedin' in session and 'cID' in session:
        return redirect(url_for('index'))
    elif 'loggedin' not in session:
        return redirect(url_for('blogin'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM package WHERE aid=%s',(session['aID'],))
    packages = cursor.fetchall()
    cursor.execute('SELECT * FROM ptag')
    ptag = cursor.fetchall()
    cursor.close()
    return render_template('bmanagePackage.html',packages=packages,ptag=ptag)

@app.route('/b/profile',methods=['GET','POST'])
def bprofile():
    if 'loggedin' in session and 'cID' in session:
        if request.method == 'GET':
            return redirect(url_for('profile'))
        elif request.method == 'POST':
            password = request.form['password']
            email = request.form['email']
            hpnum = request.form['hpnum']

            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address! Updates not done.',category='error')
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE agency set email=%s, password=%s, hpnum=%s WHERE id = %s ', (email, generate_password_hash(password), hpnum, session['aID'],))
                mysql.connection.commit() #note that you need to commit the changes for INSERT,UPDATE and DELETE statements
                cursor.close()
                flash('You have updated your email, hotline and password successfully',category='success')
    elif 'loggedin' not in session:
        return redirect(url_for('blogin'))
    return render_template('bprofile.html')

@app.route('/b/search',methods=['GET','POST'])
@app.route('/b/search/<tagname>',methods=['GET','POST'])
def bsearch(tagname=None):
    if 'loggedin' in session and 'cID' in session:
        return redirect(url_for('search'))
    elif 'loggedin' not in session:
        return redirect(url_for('blogin'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT MIN(aprice) a, MAX(aprice) b FROM package')
    cost = cursor.fetchone() 
    mincost = cost['a']
    maxcost = cost['b']
    cursor.execute('SELECT * FROM package')
    fields = ['package name','location','tags','agency']
    
    if request.method == 'POST':
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
            return render_template('bsearch.html',packages=packages, ptag=ptag, fields=fields, search=search1, maxcost=maxcost, mincost=mincost)
    elif not tagname == None:
        query = 'SELECT distinct p.* FROM package p, ptag t WHERE p.pid=t.pid and tag like %s'
        cursor.execute(query, (tagname,))
        packages = cursor.fetchall()
        cursor.execute('SELECT * FROM ptag')
        ptag = cursor.fetchall()
        cursor.close()
        return render_template('bsearch.html',packages=packages, ptag=ptag, fields=fields, maxcost=maxcost, mincost=mincost)
    else:
        packages = cursor.fetchall() #fetch all records
        cursor.execute('SELECT * FROM ptag')
        ptag = cursor.fetchall()
        cursor.close()
        return render_template('bsearch.html',packages=packages, ptag=ptag, fields=fields, maxcost=maxcost, mincost=mincost)
    return render_template('bsearch.html')

@app.route('/b/edit/<pid>',methods=['GET','POST'])
def bedit(pid):
    if 'loggedin' in session and 'cID' in session:
        return redirect(url_for('index'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        cursor.execute('SELECT p.*, aname FROM package p, agency a WHERE pid = %s and p.aid=a.aid',(str(pid),))
        package = cursor.fetchone()
        cursor.execute('SELECT r.*, concat(fname,\' \',lname) cname FROM review r, customer c WHERE pid = %s and r.cid = c.cid',(str(pid),))
        reviews = cursor.fetchall()
        cursor.close()
        return render_template('bpackage.html',package=package,reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)