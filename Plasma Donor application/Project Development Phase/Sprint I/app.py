from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import bcrypt
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vfs92883;PWD=J1eOs6y4n7xtEkUh", '', '')
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['POST', 'GET'])
def redirecttohome():
    return redirect('home')

@app.route('/home', methods=['POST', 'GET'])
def home():

    return render_template("home.html")

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    return render_template("signin.html")

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template("about.html")

@app.route('/rules', methods=['POST', 'GET'])
def rules():
    return render_template("rules.html")

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template("contact.html")

@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    return render_template("feedback.html")

@app.route('/regdonor', methods=['POST', 'GET'])
def regdonor():
    return render_template("regdonor.html")

@app.route('/done', methods=['POST', 'GET'])
def done():
    return render_template("done.html")

@app.route('/registration_confirmed', methods=['POST', 'GET'])
def registration_confirmed():
    return render_template("registration_confirmed.html")

@app.route('/confirmation', methods=['POST', 'GET'])
def confirmation():
    return render_template("confirmation.html")

@app.route('/requestdonor', methods=['POST', 'GET'])
def requestdonor():
    return render_template("requestdonor.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("entered into post")

        if not username or not password:
            return render_template('login.html', error='please fill all fields')
        sql = "select * from user where username=? and password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        dic = ibm_db.fetch_assoc(stmt)
        print(login)
        if login:
            return redirect('signin')

        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
    


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirm password']
        gender = request.form['gender']
        age = request.form['age']
        email = request.form['email']
        mobileno = request.form['mobile no']

        if not username or password or confirmpassword or gender or age or email or mobileno:
            return render_template('register.html', error='Please fill all the fields')
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = "SELECT * FROM user WHERE username=? OR password=?"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        isuser = ibm_db.fetch_assoc(stmt)
        if not isuser:
            sql = "INSERT INTO user(username, password, confirmpassword, gender, age, email, mobileno) VALUES(?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.bind_param(prep_stmt, 3, confirmpassword)
            ibm_db.bind_param(prep_stmt, 4, gender)
            ibm_db.bind_param(prep_stmt, 5, age)
            ibm_db.bind_param(prep_stmt, 6, email)
            ibm_db.bind_param(prep_stmt, 7, mobileno)
            ibm_db.execute(prep_stmt)
            return redirect(url_for('home'))
        else:
            return render_template('register.html', error='Invalid details')
    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/registerfordonor', methods=['POST', 'GET'])
def registerfordonor():

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age1 = request.form['age1']
        bloodgroup = request.form['bloodgroup']
        gender1 = request.form['gender1']
        donatedbefore = request.form['donatedbefore']
        address1 = request.form['address1']
        anyhealthissues = request.form['anyhealthissues']
        sql1 = "insert into DONORDETAILS values(?,?,?,?,?,?,?,?)"
        prep_stmt1 = ibm_db.prepare(conn, sql1)
        ibm_db.bind_param(prep_stmt1, 1, firstname)
        ibm_db.bind_param(prep_stmt1, 2, lastname)
        ibm_db.bind_param(prep_stmt1, 3, age1)
        ibm_db.bind_param(prep_stmt1, 4, bloodgroup)
        ibm_db.bind_param(prep_stmt1, 5, gender1)
        ibm_db.bind_param(prep_stmt1, 6, donatedbefore)
        ibm_db.bind_param(prep_stmt1, 7, address1)
        ibm_db.bind_param(prep_stmt1, 8, anyhealthissues)
        ibm_db.execute(prep_stmt1)
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/requestfordonor', methods=['POST', 'GET'])
def requestfordonor():

    if request.method == 'POST':
        username = request.form['username']
        gender1 = request.form['gender']
        age1 = request.form['age']
        bloodgroup = request.form['bloodgroup']
        email = request.form['email']
        mobileno = request.form['mobileno']

        if not username or gender1 or age1 or bloodgroup or email or mobileno:
            return render_template('request.html', error='Please fill all the fields')

        query = "select * from donordetails where username=? or bloodgroup=?"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, bloodgroup)
        ibm_db.execute(stmt)
        isuser = ibm_db.fetch_assoc(stmt)
        if not isuser:
            return render_template('request.html', success='Request sent successfully.')
        else:
            return render_template('request.html', error='Invalid details')
    return render_template('home.html', name='home')


if (__name__) == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
