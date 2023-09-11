from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import os
from datetime import datetime

# Initialize flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TzALB4eJ89*Ib!bn0aH28w9MFSy2iuu1!0olxkHADk2gq&PpMQ'
app.config['SESSION_COOKIE_NAME'] = 'ID'
# app.config['SESSION_COOKIE_SECURE'] = True 
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# app.config['SESSION_PERMANENT'] = False
# Connect to MYSQL database
# app.config['MYSQL_HOST'] = 'sql3.freesqldatabase.com'
# app.config['MYSQL_USER'] = 'sql3644470'
# app.config['MYSQL_DB'] = 'sql3644470'
# app.config['MYSQL_PASSWORD'] = '2g2yv7IxjY'
# app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Yoseph'
app.config['MYSQL_DB'] = 'kkhc'
app.config['MYSQL_PASSWORD'] = '1212'

# Initialize the Connection
mysql = MySQL(app)

# File uploading directory

UPLOAD_FOLDER = 'static/Attachments'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Auth

def auth():
    try:
        username, password = session["username"], session["password"]
    except Exception:
        return False
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM admin WHERE username = %s", (username,))
        dbpassword = cur.fetchall()
        dbpassword = dbpassword[0][0]
        cur.close()
        if password == dbpassword:
            return True
        return False

# Home page

@app.route('/')
def home():
    return "Home"

# Admin Home
@app.route("/admin")
def admin():
    if not auth():
        return redirect(url_for("login"))
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(id) FROM memberinfo")
        memberscount = cur.fetchall()
        memberscount = memberscount[0][0]
        cur.execute("SELECT COUNT(id) FROM children")
        childrencount = cur.fetchall()
        childrencount = childrencount[0][0]
        cur.execute("SELECT COUNT(memberid) FROM churchinfo WHERE churchrelationship = 1")
        activemembers = cur.fetchall()
        activemembers = activemembers[0][0]
        cur.close()
    except Exception as e:
        flash(f'Server error: {e}')
        return redirect(url_for('admin'))
        
    return render_template("dashboard.html", memberscount = memberscount, childrencount = childrencount, activemembers = activemembers)


# Login for Admins
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM admin WHERE username = %s", (username,))
        admin = cur.fetchall()
        cur.close()
        try:
            dbpassword = admin[0][0]
            
        except Exception:
            flash("Username Not Found!")
            return redirect(url_for('login'))
        else:
            if password == dbpassword:
                session["username"] = username
                session["password"] = password
                return redirect(url_for("admin"))
            else:
                flash("Password Incorrect!")
                return redirect(url_for('login'))
    return render_template("login.html")

# Add new member

@app.route('/addmember', methods=['GET', 'POST'])
def addmember():
    if not auth():
        return redirect(url_for("login"))    
    if request.method == "POST":
        try:
            if 'profile' in request.files:
                profile = request.files['profile']
            title = request.form["title"]
            f_name = request.form["f_name"]
            m_name = request.form["m_name"]
            l_name = request.form["l_name"]
            sex = request.form["sex"]
            dob = request.form["dob"]
            mob = request.form["mob"]
            yob = request.form["yob"]
            handicap = request.form['handicap']
            if handicap == 'false':
                handicap = 0
            else:
                handicap = 1       
            description = request.form["description"]
            subcity = request.form['subcity']
            district = request.form['district']
            house_no = request.form['house_no']
            other_name = request.form['other_name']
            phone = request.form['phoneNumber1']
            homephone = request.form['phoneNumber2']
            email = request.form["email"]
            dobaptism = request.form["dobaptism"]
            mobaptism = request.form["mobaptism"]
            yobaptism = request.form["yobaptism"]
            bap_where = request.form["bap_where"]
            domembership = request.form["domembership"]
            momembership = request.form["momembership"]
            yomembership = request.form["yomembership"]
            inchurch = request.form["inchurch"]
            if inchurch == 'false':
                inchurch = 0
            else:
                inchurch = 1  
            service = request.form["service"]
            if service == "true":
                service = {}
                if 'singer' in request.form:
                    service[request.form["singer"]] = request.form['status1']
                if 'children' in request.form:
                    service[request.form["children"]] = request.form['status2']
                if 'prayer' in request.form:
                    service[request.form["prayer"]] = request.form['status3']
                if 'youth' in request.form:
                    service[request.form["youth"]] = request.form['status4']
                if 'sisters' in request.form:
                    service[request.form["sisters"]] = request.form['status5']
                if 'outreach' in request.form:
                    service[request.form["outreach"]] = request.form['status6']
                if 'deacon' in request.form:
                    service[request.form["deacon"]] = request.form['status7']
                if 'charity' in request.form:
                    service[request.form["charity"]] = request.form['status8']
                if 'eddir' in request.form:
                    service[request.form["eddir"]] = request.form['status9']
                if 'elder' in request.form:
                    service[request.form["elder"]] = request.form['status10']
            educheck = request.form['educheck']
            if educheck == 'true':
                level = request.form["edu_status_list"]
                field = request.form["sub_of_study"]
            work_stats = request.form["work_stats"]
            if work_stats == 'true':
                work_stats = 1
                work_type = request.form["work_type"]
                work_place = request.form["work_place"]
                responsibility = request.form["responsibility"]
                profession = request.form['profession']
                talent = request.form["talent"]
            else:
                work_stats = 0
            mstats = request.form['mstats']
            if mstats == "true":
                sFName = request.form['sFName']
                sMName = request.form['sMName']
                sLName = request.form['sLName']
                shere = request.form['shere']
            
            
        except KeyError as e:
            flash(f"Missing or incorrect form field: {e}")
            return redirect(url_for('addmember'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for("addmember"))
            

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO memberinfo (title, firstname, middlename, lastname, sex, birthdate, subcity, district, homeno, neighborhood, Homephone, personalphone, email, handicap, handicaptype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (title, f_name, m_name, l_name, sex, dob, subcity, district, house_no, other_name, homephone, phone, email, handicap, description))
            mysql.connection.commit()
            cur.execute("SELECT id FROM memberinfo WHERE firstname = %s AND middlename = %s AND lastname = %s ORDER BY id DESC", (f_name, m_name, l_name))
            userid = cur.fetchall()
            userid = userid[0][0]
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO churchinfo (memberid, baptizmdate, baptizedwhere, dateofmembership, churchrelationship) VALUES (%s, %s, %s, %s, %s)", (userid, bap_date, bap_where, mem_date, inchurch))
            mysql.connection.commit()
            if service == "true":
                for key, value in service.items():
                    cur.execute("INSERT INTO serviceinfo(memberid, serviceid, isactive) VALUES (%s, %s, %s)", (userid, key, value))
                    mysql.connection.commit()
            if educheck == 'true':
                cur.execute("INSERT INTO education(memberid, field, edulevel) VALUES (%s, %s, %s)", (userid, field, level))
                mysql.connection.commit()
            if work_stats == 1:
                cur.execute("INSERT INTO workinfo(memberid, work, worktype, place, responsiblility, proffesion, talent) VALUES(%s, %s, %s, %s, %s, %s, %s)", (userid, work_stats, work_type, work_place, responsibility, profession, talent))
                mysql.connection.commit()
            # if mstats == 'true':
            #     cur.execute("INSERT INTO marriage(husband_id, spouseinchurch, spousefname, spousemname, spouselname) VALUES(%s, %s, %s, %s, %s)", (userid, shere, sFName, sMName, sLName))
            #     mysql.connection.commit()
            if 'profile' in request.files and profile.filename != '':
                profile.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{userid}.jpg'))
                cur.execute("INSERT INTO files (memberid, picture) VALUES (%s, %s)", (userid, f'{userid}.jpg'))
                mysql.connection.commit()
                cur.close()

        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('addmember'))
        flash('Form Submitted Successfully!')
        return redirect(url_for("addmember"))
    return render_template('addmember.html')

# Members list
@app.route('/members')
def members():
    if not auth():
        return redirect(url_for("login"))
        # today = datetime.today()
        # today = today.strftime('%Y-%m-%d')
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, firstname, middlename, lastname, subcity, personalphone, churchrelationship FROM memberinfo LEFT JOIN churchinfo ON id = memberid")
    members = cur.fetchall()
    cur.close()
    return render_template('memberslist.html', members = members)
        

# Add new children
@app.route("/addchild", methods=["GET", "POST"])
def addchild():
    return render_template("addchild.html")


# Analysis
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

# Members detail stats
@app.route("/member/<int:id>", methods=['GET', 'POST'])
def member(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from memberinfo left join churchinfo on id = memberid where id = {id}")
        member = cur.fetchall()
        member = member[0]
        cur.close()
    except IndexError:
        return redirect('../members')
    except Exception as e:
        return f"Error occured: {e}"

    return render_template("memberdetail.html", member = member)


@app.route("/member/<int:id>/edit", methods=['GET', 'POST'])
def editmember(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * from memberinfo where id = {id}")
    member = cur.fetchall()
    member = member[0]
    cur.close()
    return render_template('editmember.html', member = member)
    

# Children list
@app.route("/children")
def children():
    return "Children list"


if __name__ == "__main__":
    app.run(debug=True)

