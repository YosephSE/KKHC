from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import os
from datetime import datetime

# Initialize flask
app = Flask(__name__)
app.secret_key = 'TzALB4eJ89*Ib!bn0aH28w9MFSy2iuu1!0olxkHADk2gq&PpMQ'

# Connect to MYSQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1212'
app.config['MYSQL_DB'] = 'kkhc'

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
    if auth():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(id) FROM memberinfo")
        memberscount = cur.fetchall()
        memberscount = memberscount[0][0]
        cur.execute("SELECT COUNT(id) FROM children")
        childrencount = cur.fetchall()
        childrencount = childrencount[0][0]

        cur.close()
    else:
        return redirect(url_for("login"))
    return render_template("dashboard.html", memberscount = memberscount, childrencount = childrencount)


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
            return "Username not found!"
        else:
            if password == dbpassword:
                session["username"] = username
                session["password"] = password
                return redirect(url_for("admin"))
            else:
                return f"passwrod incorrect!"
    return render_template("login.html")

# Add new member

@app.route('/addmember', methods=['GET', 'POST'])
def addmember():
    if auth():        
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
                handicap = request.form['handicap']            
                description = request.form["description"]
                subcity = request.form['subcity']
                district = request.form['district']
                house_no = request.form['house_no']
                other_name = request.form['other_name']
                phone = request.form['phoneNumber1']
                homephone = request.form['phoneNumber2']
                email = request.form["email"]
                bap_date = request.form["bap_date"]
                bap_where = request.form["bap_where"]
                mem_date = request.form["mem_date"]
                # service = request.form["service"]
                # churchrelation = request.form["churchrelation"]
                # if service == "1":
                #     singer = request.form["singer"]
                #     children = request.form["children"]
                #     prayer = request.form["prayer"]
                #     # youth = request.form["youth"]
                #     girls = request.form["girls"]
                #     outreach = request.form["outreach"]
                #     deacon = request.form["deacon"]
                #     charity = request.form["charity"]
                #     eddir = request.form["eddir"]
                    # elder = request.form["elder"]
                    # print(singer, children, prayer, girls, outreach, deacon, charity, eddir)
            except KeyError as e:
                return f"Missing or incorrect form field:2 {e}"
            except Exception as e:
                return f"An error occurred: {e}"
            

            try:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO memberinfo (title, firstname, middlename, lastname, sex, birthdate, subcity, district, homeno, neighborhood, Homephone, personalphone, email, handicap, handicaptype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (title, f_name, m_name, l_name, sex, dob, subcity, district, house_no, other_name, homephone, phone, email, handicap, description))
                mysql.connection.commit()
                cur.execute("SELECT id FROM memberinfo WHERE firstname = %s AND middlename = %s AND lastname = %s ORDER BY id DESC", (f_name, m_name, l_name))
                userid = cur.fetchall()
                userid = userid[0][0]
                cur.close()
                cur = mysql.connection.cursor()
                # cur.excute("INSERT INTO services(memberid, serviceid, isactive) VALUES ()")
                # cur.execute("INSERT INTO churchinfo (memberid, baptizmdate, baptizedwhere, dateofmembership) VALUES (%s, %s, %s, %s)", (userid, bap_date, bap_where, mem_date))
                # mysql.connection.commit()
                    # Change file name
                if 'profile' in request.files and profile.filename != '':
                    profile.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{userid}.jpg'))
                    cur.execute("INSERT INTO files (memberid, picture) VALUES (%s, %s)", (userid, f'{userid}.jpg'))
                    mysql.connection.commit()
                    cur.close()
            except Exception as e:
                return f"An error occurred: {e}"

            return 'Form submitted successfully!'
    else:
        return redirect(url_for("login"))
    return render_template('addmember.html')

# Members list
@app.route('/members')
def members():
    if auth():
        today = datetime.today()
        today = today.strftime('%Y-%m-%d')
        cur = mysql.connection.cursor()
        cur.execute("SELECT firstname, middlename, lastname, subcity, personalphone, picture FROM memberinfo left join files on id = memberid")
        members = cur.fetchall()
        cur.close()
        return render_template('memberslist.html', members = members)
    else:
        return redirect(url_for("login"))

# Add new children
@app.route("/newchild", methods=["GET", "POST"])
def newchild():
    return "newchild"


# Analysis
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

# Children list
@app.route("/children")
def children():
    return "Children list"
if __name__ == "__main__":
    app.run(debug=True)

