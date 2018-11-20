from flask import Flask, render_template
import pymysql.cursors

app = Flask(__name__)

conn_sql = pymysql.connect(host='localhost',
                           port=3306,
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, hashlib.sha1(password.encode('utf-8')).hexdigest()))
    data = cursor.fetchone()

    cursor.close()
    error = None

    if(data):
        session['username'] = username
        return redirect(url_for('home'))
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

@app.route('/register')
def register():
    return render_template('register.html')
  
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    cursor = conn.cursor()
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = None
    
    if(data):
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (username, hashlib.sha1(password.encode('utf-8')).hexdigest(),first_name,last_name))
        conn.commit()
        cursor.close()
        return render_template('index.html')



@app.route('/public_content', methods=['GET', 'POST'])
def public_content():
    cursor = conn_sql.cursor();
    query = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('public_content.html', post=data)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
