from flask import Flask, render_template, request, redirect, session, url_for,flash
import pymysql.cursors
import hashlib

app = Flask(__name__)

conn_sql = pymysql.connect(host='localhost',
                           port=8889,
                           user='root',
                           password='root',
                           db='pricosha',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    email = request.form['email']
    password = request.form['password']

    cursor = conn_sql.cursor()
    query = 'SELECT * FROM Person WHERE email = %s and password = %s'
    cursor.execute(query, (email, hashlib.sha1(password.encode('utf-8')).hexdigest()))
    data = cursor.fetchone()

    cursor.close()
    error = None

    if (data):
        session['email'] = email
        return redirect(url_for('home'))
    else:
        error = 'Invalid login or email'
        return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    cursor = conn_sql.cursor()
    query = 'SELECT * FROM Person WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchone()
    error = None

    if (data):
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (email, hashlib.sha1(password.encode('utf-8')).hexdigest(), first_name, last_name))
        conn_sql.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    email = session['email']
    cursor = conn_sql.cursor()
    query = 'SELECT item_id, email, post_time, file_path, item_name FROM ContentItem WHERE post_time >= NOW() - \
    INTERVAL 1 DAY AND is_pub = 1'
    name = 'SELECT first_name, last_name FROM person WHERE email= %s '
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.execute(name, (email))
    names = cursor.fetchall()
    cursor.close()
    return render_template('home.html', post=data, firstname=names[0]['first_name'], lastname=names[0]['last_name'])

@app.route('/share')
def share():
    return render_template('share.html')

@app.route('/shareAuth',methods=['GET', 'POST'])
def shareAuth():
    item_name = request.form['item_name']
    file_path = request.form['file_path']
    email = session['email']
    public = request.form['public']
    
    #gets mostrecentID
    
    cursor = conn_sql.cursor()
    query = 'SELECT max(item_id) as lastID FROM ContentItem'
    cursor.execute(query)
    data = cursor.fetchone()
    if(data):
        item_id = data["lastID"] + 1
    else:
        item_id = 0
    error = None

    if(public):
        public = 1
    else:
        public = 0
    
    ins = 'INSERT INTO ContentItem VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(ins,(item_id,email,None,file_path,item_name, public))
    conn_sql.commit()
    cursor.close()

    message = "Shared!"
    return redirect(url_for('home'))

@app.route('/addFriend')
def addFriend():
    return render_template('addFriend.html')

@app.route('/addFriendAuth', methods = ['GET','POST'])
def addFriendAuth():
    fg_name = request.form['fg_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    mem_email = request.form['mem_email']
    creator_email = session['email']


    cursor = conn_sql.cursor()
    #checks for exisiting friend group
    checkquery = "SELECT fg_name FROM FriendGroup WHERE fg_name = %s AND email = %s"
    cursor.execute(checkquery,(fg_name,creator_email))
    checkfg = cursor.fetchone()

    #checks for exisiting person
    checkquery = "SELECT first_name, last_name, email FROM Person WHERE first_name = %s AND last_name = %s AND email = %s"
    cursor.execute(checkquery,(first_name,last_name,mem_email))
    checkper = cursor.fetchone()


    if(checkfg is not None and checkper is not None):
    #checks if person is in friendgroup
        checkquery = "SELECT member_email FROM Belong WHERE member_email = %s AND creator_email = %s AND fg_name = %s"
        cursor.execute(checkquery,(mem_email,creator_email,fg_name))
        checkboth = cursor.fetchone()
        if(checkboth):
            error = "Friend is already in group!"
            cursor.close()
            return render_template('addFriend.html', error=error)
        else:
            ins = "INSERT INTO Belong VALUES (%s,%s,%s)"
            cursor.execute(ins,(mem_email,fg_name,creator_email))
            conn_sql.commit()
            cursor.close()
            flash("Friend has been added!")
            return render_template('addFriend.html')
    else:
        cursor.close()
        error = "Friend Group or Person does not exist!"
        return render_template('addFriend.html', error=error)
    
'''
@app.route('/sharefg')
def sharefg():
    return render_template('sharefg.html')

@app.route('/sharefgAuth',methods = ['GET','POST'])
def sharefgAuth():
    email = session['email']
    friend_group = request.form['friend_group']

    cursor = conn_sql.cursor()
    query = 'SELECT max(item_id) as lastID FROM ContentItem WHERE email = %s'
    cursor.execute(query,(email))
    data = cursor.fetchone()
    item_id = data["lastID"]
    query2 = 'SELECT fg_name FROM Share WHERE fg_name = %s'
    cursor.execute(query2,(friend_group))
    data = cursor.fetchone()
    if(data):
        ins = 'INSERT INTO Share VALUES (%s,%s,%s)'
        cursor.execute(ins,(friend_group,item_id,email))
    cursor.close()
    return render_template('home.html')
'''

app.secret_key = 'FDSJKGSEW'

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
