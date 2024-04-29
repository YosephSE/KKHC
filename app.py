from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
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
# app.config['MYSQL_HOST'] = 'sql9.freesqldatabase.com'
# app.config['MYSQL_USER'] = 'sql9647331'
# app.config['MYSQL_DB'] = 'sql9647331'
# app.config['MYSQL_PASSWORD'] = '3TWIARJRNk'
# app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "Yoseph"
app.config["MYSQL_PASSWORD"] = "1212"
app.config["MYSQL_DB"] = "kkhc"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

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
        if datetime.now().month > 8:
            year = datetime.now().year - 7
        else:
            year = datetime.now().year - 8
        upperbound = year - 15
        lowerbound = year - 35
        cur.execute(f"SELECT COUNT(id) from memberinfo WHERE birthyear BETWEEN {lowerbound} AND {upperbound}")
        youth = cur.fetchall()[0][0]
        cur.close()
    except Exception as e:
        flash(f'Server error: {e}')
        return redirect(url_for('admin'))
        
    return render_template("dashboard.html", youth = youth, memberscount = memberscount, childrencount = childrencount, activemembers = activemembers)


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
        # try:
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
            description = ''
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
            services = {}
            if 'singer' in request.form:
                services[request.form["singer"]] = request.form['status1']
            if 'children' in request.form:
                services[request.form["children"]] = request.form['status2']
            if 'prayer' in request.form:
                services[request.form["prayer"]] = request.form['status3']
            if 'youth' in request.form:
                services[request.form["youth"]] = request.form['status4']
            if 'sisters' in request.form:
                services[request.form["sisters"]] = request.form['status5']
            if 'outreach' in request.form:
                services[request.form["outreach"]] = request.form['status6']
            if 'deacon' in request.form:
                services[request.form["deacon"]] = request.form['status7']
            if 'charity' in request.form:
                services[request.form["charity"]] = request.form['status8']
            if 'eddir' in request.form:
                services[request.form["eddir"]] = request.form['status9']
            if 'elder' in request.form:
                services[request.form["elder"]] = request.form['status10']
            if "educheck" in request.form:
                print(345678)
            else:
                print("string")
            # educheck = request.form["educheck"]
            # print(educheck)
            # if educheck == 'true':
            #     level = request.form["edu_status_list"]
            #     field = request.form["sub_of_study"]
            #     print(level, field)
            # else:
            #     print("NO edu")
            work_stats = request.form["work_stats"]
            if work_stats == 'true':
                work_stats = 1
                work_type = request.form["work_type"]
                work_place = request.form["work_place"]
                responsibility = request.form["responsiblity"]
                profession = request.form['profession']
                talent = request.form["talent"]
                print(work_stats, work_type, work_place, responsibility, profession, talent)
            else:
                work_stats = 0
            mstats = request.form['mstats']
            if mstats == "true":
                stitle = request.form['stitle']
                sfname = request.form['sfname']
                smname = request.form['smname']
                slname = request.form['slname']
                merdate, mermonth, meryear = request.form['merdate'], request.form['mermonth'], request.form['meryear']
                sinchurch = request.form['sinchurch']
                shere = request.form['here']
                if sinchurch == "true" and shere == "true":
                    if 'sprofile' in request.files:
                        sprofile = request.files['sprofile']
                    # sex = request.form["sex"]
                    # sdob = request.form["sdob"]
                    # smob = request.form["smob"]
                    # syob = request.form["syob"]
                    # shandicap = request.form['shandicap']
                    # if handicap == 'false':
                    #     handicap = 0
                    #     description = ''
                    # else:
                    #     handicap = 1       
                    #     description = request.form["sdescription"]
                    # sphone = request.form['phoneNumber1']
                    # semail = request.form["semail"]
                    sdobaptism = request.form["sdobaptism"]
                    smobaptism = request.form["smobaptism"]
                    syobaptism = request.form["syobaptism"]
                    sbap_where = request.form["sbap_where"]
                    sdomembership = request.form["sdomembership"]
                    smomembership = request.form["smomembership"]
                    syomembership = request.form["syomembership"]
                    sservice = request.form["s_service"]
                    if sservice == "true":
                        sservices = {}
                        if 'ssinger' in request.form:
                            services[request.form["ssinger"]] = request.form['s_status1']
                        if 'schildren' in request.form:
                            services[request.form["schildren"]] = request.form['s_status2']
                        if 'sprayer' in request.form:
                            services[request.form["sprayer"]] = request.form['s_status3']
                        if 'syouth' in request.form:
                            services[request.form["syouth"]] = request.form['s_status4']
                        if 'ssisters' in request.form:
                            services[request.form["ssisters"]] = request.form['s_status5']
                        if 'soutreach' in request.form:
                            services[request.form["soutreach"]] = request.form['s_status6']
                        if 'sdeacon' in request.form:
                            services[request.form["sdeacon"]] = request.form['s_status7']
                        if 'scharity' in request.form:
                            services[request.form["scharity"]] = request.form['s_status8']
                        if 'seddir' in request.form:
                            services[request.form["seddir"]] = request.form['s_status9']
                        if 'selder' in request.form:
                            services[request.form["selder"]] = request.form['s_status10']
                        print("spouse in this church!")
                    
                elif sinchurch == "true" and shere == "false":
                    schurch = request.form['schurch']
                    print("spouse in other church!")
                    

            #     sphoneNumber = request.form['sphoneNumber']
                # semail = request.form['semail']
                # sdob, smob, syob = request.form['sdob'], request.form['smob'], request.form['syob']


            
        # except KeyError as e:
        #     flash(f"Missing or incorrect form field: {e}")
        #     return redirect(url_for('addmember'))
        # except Exception as e:
        #     flash(f"An error occurred: {e}")
        #     return redirect(url_for("addmember"))
            

        # try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO memberinfo (title, firstname, middlename, lastname, sex, birthdate, birthmonth, birthyear, subcity, district, homeno, neighborhood, Homephone, personalphone, email, handicap, handicaptype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (title, f_name, m_name, l_name, sex, dob, mob, yob, subcity, district, house_no, other_name, homephone, phone, email, handicap, description))
        mysql.connection.commit()
        cur.execute("SELECT id FROM memberinfo WHERE firstname = %s AND middlename = %s AND lastname = %s ORDER BY id DESC", (f_name, m_name, l_name))
        userid = cur.fetchall()
        userid = userid[0][0]
        cur.execute("INSERT INTO churchinfo (memberid, baptizmdate, baptizmmonth, baptizmyear, baptizedwhere, dateofmembership, monthofmembership, yearofmembership, churchrelationship) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (userid, dobaptism, mobaptism, yobaptism, bap_where, domembership, momembership, yomembership, inchurch))
        mysql.connection.commit()
        if service == "true":
            for key, value in services.items():
                cur.execute("INSERT INTO serviceinfo(memberid, serviceid, isactive) VALUES (%s, %s, %s)", (userid, key, value))
                mysql.connection.commit()
        # if educheck == 'true':
        #     cur.execute("INSERT INTO education(memberid, field, edulevel) VALUES (%s, %s, %s)", (userid, field, level))
        #     mysql.connection.commit()
        # if work_stats == 1:
        #     cur.execute("INSERT INTO workinfo(memberid, work, worktype, place, responsiblility, proffesion, talent) VALUES(%s, %s, %s, %s, %s, %s, %s)", (userid, work_stats, work_type, work_place, responsibility, profession, talent))
        #     mysql.connection.commit()
        # elif work_stats == 0:
        #     cur.execute("INSERT INTO workinfo(memberid, work) VALUES(%s, %s)", (userid, 0))
        #     mysql.connection.commit()
            # if mstats == 'true':
            #     cur.execute("INSERT INTO marriage(husband_id, spouseinchurch, spousefname, spousemname, spouselname) VALUES(%s, %s, %s, %s, %s)", (userid, shere, sFName, sMName, sLName))
            #     mysql.connection.commit()
            # cur.close()
        if 'profile' in request.files and profile.filename != '':
            profile.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{userid}.jpg'))
            

        # except Exception as e:
        #     flash(f"An error occurred: {e}")
        #     return redirect(url_for('addmember'))
        flash('Form Submitted Successfully!')
        return redirect(url_for("addmember"))
    return render_template('addmember.html')

# Members list
@app.route('/members')
def members():
    if not auth():
        return redirect(url_for("login"))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, firstname, middlename, lastname, subcity, personalphone, churchrelationship FROM memberinfo LEFT JOIN churchinfo ON memberinfo.id = churchinfo.memberid ORDER BY firstname")
    members = cur.fetchall()
    cur.close()
    return render_template('memberslist.html', members = members)
        

# Add new children
@app.route("/addchild", methods=["GET", "POST"])
def addchild():
    if not auth():
        return redirect(url_for("login"))
    if request.method == 'POST':
        try:
            f_name = request.form["f_name"]
            m_name = request.form["m_name"]
            l_name = request.form["l_name"]
            sex = request.form["sex"]
            dob = request.form["dob"]
            mob = request.form["mob"]
            yob = request.form["yob"]
            dvbs = request.form['dvbs_edu_status_list']
            sunday = request.form['sunday']
            grade = request.form['grade_level']
            parent = request.form['parent_here']
            if parent == 'true':
                fatherid = request.form['parent1_fo_key']
                motherid = request.form['parent2_fo_key']
                fatherid = fatherid[0:fatherid.index(' ')]
                motherid = motherid[0:motherid.index(' ')]
                
            else:
                father = request.form['father_n']
                mother = request.form['mother_n']
                church = request.form['parent_church']
                motherphone = request.form['mphoneNumber']
                fatherphone = request.form['fphoneNumber']
        except Exception as e:
            flash(f"Missing: {e}")
            redirect(url_for("addchild"))

        try:
            cur = mysql.connection.cursor()
            if parent == 'true':
                cur.execute("INSERT INTO children (firstname, middlename, lastname, sex, birthdate, birthmonth, birthyear, sundayschoollevel, dvbslevel, grade, motherid, fatherid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (f_name, m_name, l_name, sex, dob, mob, yob, sunday, dvbs, grade, motherid, fatherid))
            else:
                cur.execute("INSERT INTO children (firstname, middlename, lastname, sex, birthdate, birthmonth, birthyear, sundayschoollevel, dvbslevel, grade, mothername, fathername, familychurch, motherphone, fatherphone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (f_name, m_name, l_name, sex, dob, mob, yob, sunday, dvbs, grade, mother, father, church, motherphone, fatherphone))
            mysql.connection.commit()
        except Exception as e:
            flash(f'Internal Server Error: {e}')
            redirect(url_for("addchild"))
        else:
            flash("Form submitted successfully!")
            redirect(url_for("addchild"))
        
    return render_template("addchild.html")


# Analysis
@app.route("/analysis")
def analysis():
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
        
        if datetime.now().month > 8:
            year = datetime.now().year - 7
        else:
            year = datetime.now().year - 8
        upperbound = year - 15
        lowerbound = year - 35
        cur.execute(f"SELECT COUNT(id) from memberinfo WHERE birthyear BETWEEN {lowerbound} AND {upperbound}")
        youth = cur.fetchall()[0][0]
        cur.close()
        
    except Exception as e:
        flash(f'Server error: {e}')
        return redirect(url_for('analysis'))
        
    return render_template("analysis.html", youth = youth, memberscount = memberscount, childrencount = childrencount, activemembers = activemembers)


# Members detail stats
@app.route("/member/<int:id>", methods=['GET', 'POST'])
def member(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from memberinfo inner join churchinfo on memberinfo.id = churchinfo.memberid  left join education on memberinfo.id = education.memberid inner join workinfo on memberinfo.id = workinfo.memberid where memberinfo.id = {id}")
        member = cur.fetchall()[0]
        cur = mysql.connection.cursor()
        cur.execute(f"select service, isactive from serviceinfo inner join services on serviceid = services.id where memberid = {id}")
        services = cur.fetchall()
        cur.close()

        try:
            # Marriage info
            cur = mysql.connection.cursor()
            cur.execute(f"select id, husband_id, wife_id, weddingdate, weddingmonth, weddingyear from marriage where husband_id = {id} or wife_id = {id}")
            mstat = cur.fetchall()[0]
            cur.close()
            # Checks if both are in this church
            if mstat[1] != None and mstat[2] != None:
                # Checks if the member is husband or wife
                if mstat[1] == id:
                    cur = mysql.connection.cursor()
                    cur.execute(f"SELECT id, firstname, middlename FROM memberinfo WHERE id = {mstat[2]}")
                    spouse = cur.fetchall()[0]
                    cur.close()
                elif mstat[2] == id:
                    cur = mysql.connection.cursor()
                    cur.execute(f"SELECT id, firstname, middlename FROM memberinfo WHERE id = {mstat[1]}")
                    spouse = cur.fetchall()[0]
                    cur.close()
            # if one of them are not in church
            elif mstat[1] == None or mstat[2] == None:
                cur = mysql.connection.cursor()
                cur.execute(f"SELECT spousefname, spousemname, spouseinchurch, spousechurch FROM marriage WHERE id = {mstat[0]}")
                spouse = cur.fetchall()[0]
        except IndexError:
            mstat = None
            spouse = None
        except Exception as e:
            flash(f"Error occured: {e}")
            mstat = None
            spouse = None
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"select firstname, middlename, lastname from children where motherid = {id} or fatherid = {id}")
            children = cur.fetchall()
            cur.close()
        except IndexError:
            children = None
        except Exception:
            children = None
        cur.close()
    except IndexError:
        flash("USER NOT FOUND!")
        return redirect('../members')
    except Exception as e:
        flash(f"Error occured: {e}")
        return redirect('../members')

    return render_template("memberdetail.html", member = member, mstat = mstat, services = services, children = children, spouse = spouse)


@app.route("/member/<int:id>/edit", methods=['GET', 'POST'])
def editmember(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * from memberinfo where memberinfo.id = {id}")
    member = cur.fetchall()[0]
    # member = member[0]
    cur.close()
    return render_template('editmember.html', member = member)
    

# Children list
@app.route("/children")
def children():
    cur = mysql.connection.cursor()
    cur.execute("select * from children order by firstname")
    children = cur.fetchall()
    return render_template("childrenlist.html", children = children)

@app.route("/child/<int:id>", methods=['GET', 'POST'])
def child(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from children where id = {id}")
        child = cur.fetchall()[0]
    except IndexError:
        flash("Child Not Found!")
        return redirect(url_for('children'))
    if child[11] != None and child[12] != None:
        cur.execute(f"select id, firstname, middlename from memberinfo where id = {child[11]}")
        mother = cur.fetchall()[0]
        cur.execute(f"select id, firstname, middlename from memberinfo where id = {child[12]}")
        father = cur.fetchall()[0]
    else:
        mother, father = None, None

    cur.close()
    return render_template('childDetail.html', child = child, mother = mother, father = father)


@app.route("/child/<int:id>/edit", methods=['GET', 'POST'])
def editchild(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * from children where id = {id}")
    child = cur.fetchall()[0]
    cur.close()
    if request.method == 'POST':
        try:
            f_name = request.form["f_name"]
            m_name = request.form["m_name"]
            l_name = request.form["l_name"]
            sex = request.form["sex"]
            dob = request.form["dob"]
            mob = request.form["mob"]
            yob = request.form["yob"]
            dvbs = request.form['dvbs_edu_status_list']
            sunday = request.form['sunday']
            grade = request.form['grade_level']
            parent = request.form['parent_here']
            if parent == 'true':
                fatherid = request.form['parent1_fo_key']
                motherid = request.form['parent2_fo_key']
                fatherid = fatherid[0:fatherid.index(' ')]
                motherid = motherid[0:motherid.index(' ')]
                
            else:
                father = request.form['father_n']
                mother = request.form['mother_n']
                church = request.form['parent_church']
                motherphone = request.form['mphoneNumber']
                fatherphone = request.form['fphoneNumber']
        except Exception as e:
            flash(f"Missing: {e}")
            redirect(url_for("addchild"))

        try:
            cur = mysql.connection.cursor()
            if parent == 'true':
                cur.execute("UPDATE children SET firstname = %s, middlename = %s, lastname = %s, sex = %s, birthdate = %s, birthmonth = %s, birthyear = %s, sundayschoollevel = %s, dvbslevel = %s, grade = %s, motherid = %s, fatherid = %s WHERE id = %s",(f_name, m_name, l_name, sex, dob, mob, yob, sunday, dvbs, grade, motherid, fatherid, id))

            else:
                cur.execute("UPDATE children SET firstname = %s, middlename = %s, lastname = %s, sex = %s, birthdate = %s, birthmonth = %s, birthyear = %s, sundayschoollevel = %s, dvbslevel = %s, grade = %s, mothername = %s, fathername = %s, familychurch = %s, motherphone = %s, fatherphone = %s WHERE id = %s",(f_name, m_name, l_name, sex, dob, mob, yob, sunday, dvbs, grade, mother, father, church, motherphone, fatherphone, id))
                mysql.connection.commit()
        except Exception as e:
            flash(f'Internal Server Error: {e}')
            return redirect(url_for("children"))
        else:
            flash("Form submitted successfully!")
            return redirect(url_for("children"))

    return render_template('editchild.html', child = child)

@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    searchbox = request.form.get("text")
    cursor = mysql.connection.cursor()
    query = "SELECT id, firstname, middlename, lastname FROM memberinfo WHERE firstname LIKE %s ORDER BY firstname"
    cursor.execute(query, (searchbox + '%',))
    result = cursor.fetchall()

    # Convert the result tuple to a list of dictionaries
    result_list = []
    for row in result:
        result_dict = {
            'id': row[0],
            'firstname': row[1],
            'middlename': row[2],
            'lastname': row[3]
        }
        result_list.append(result_dict)

    return jsonify(result_list)

if __name__ == "__main__":
    app.run(debug=True)

