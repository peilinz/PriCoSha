from flask import Flask, render_template, request, redirect, session, url_for
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
    url = request.form['url']
    public = request.form['public']
    email = session['email']
    
    #gets mostrecentID
    cursor = conn_sql.cursor()
    query = 'SELECT max(item_id) FROM ContentItem'
    cursor.execute(query)
    data = cursor.fetchone()
    error = None
    
    if (data == None):
        item_id = 0
    else:
        print(data)
        item_id = data+1
    if (public):
        public = 1
        ins = 'INSERT INTO ContentItem VALUES(%d,%s,timestamp_value,%s,%s,%s)'
        cursor.execute(ins,(item_id,email,CURRENT_TIMESTAMP,url,item_name, public))
        cursor.commit()
        cursor.close()
        return render_template('home.html')
    else:
        public = 0
        ins = 'INSERT INTO ContentItem VALUES(%d,%s,timestamp_value,%s,%s,%s)'
        cursor.execute(ins,(item_id,email,CURRENT_TIMESTAMP,url,item_name, public))



app.secret_key = 'FDSJKGSEW'

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
