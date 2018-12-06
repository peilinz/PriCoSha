from flask import Flask, render_template, request, redirect, session, url_for, flash
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
    name = 'SELECT first_name, last_name FROM person WHERE email= %s '
    # View public contents
    query = 'SELECT item_id, email, post_time, file_path, item_name FROM ContentItem WHERE post_time >= NOW() - \
    INTERVAL 1 DAY AND is_pub = 1 ORDER BY post_time DESC'
    # View group posts
    group_post = 'SELECT DISTINCT item_id, email, post_time, file_path, item_name FROM ContentItem AS c ' \
                 'NATURAL JOIN share NATURAL JOIN belong WHERE item_id IN ' \
                 '(SELECT item_id FROM share AS s NATURAL JOIN belong ' \
                 'WHERE s.email IN (SELECT member_email FROM belong WHERE fg_name = s.fg_name ' \
                 'AND fg_name IN (SELECT fg_name FROM belong WHERE member_email= %s) AND ' \
                 'belong.creator_email = (SELECT creator_email FROM belong ' \
                 'WHERE member_email= %s))) ORDER BY post_time DESC'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.execute(name, email)
    names = cursor.fetchall()
    cursor.execute(group_post, (email, email))
    all_p = cursor.fetchall()
    cursor.close()
    return render_template('home.html', post=data, firstname=names[0]['first_name'],
                           lastname=names[0]['last_name'], all_posts=all_p)


# Post a Content Item
@app.route('/share')
def share():
    return render_template('share.html')


@app.route('/shareAuth', methods=['GET', 'POST'])
def shareAuth():
    item_name = request.form['item_name']
    file_path = request.form['file_path']
    email = session['email']

    # gets most recent ID
    cursor = conn_sql.cursor()

    query = 'SELECT max(item_id) as lastID FROM ContentItem'
    cursor.execute(query)
    data = cursor.fetchone()
    if (data):
        item_id = data["lastID"] + 1
    else:
        item_id = 0

    ins = 'INSERT INTO ContentItem VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(ins, (item_id, email, None, file_path, item_name, 1))
    conn_sql.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/sharePri')
def sharePri():
    return render_template('sharePri.html')


@app.route('/sharePriAuth', methods=['GET', 'POST'])
def sharePriAuth():
    item_name = request.form['item_name']
    file_path = request.form['file_path']
    fg_name = request.form['fg_name']
    fg_list = fg_name.split(', ')
    email = session['email']

    cursor = conn_sql.cursor()
    query = 'SELECT max(item_id) as lastID FROM ContentItem'
    cursor.execute(query)
    data = cursor.fetchone()
    if (data):
        item_id = data["lastID"] + 1
    else:
        item_id = 0

    check_if_in = 'SELECT fg_name FROM Belong WHERE fg_name = %s AND member_email = %s'
    cursor.execute(check_if_in, (fg_list[0],email))
    checkdata = cursor.fetchone()

    if(checkdata):
        # Adds to content item
        ins = 'INSERT INTO ContentItem VALUES (%s,%s,%s,%s,%s,%s)'
        cursor.execute(ins, (item_id, email, None, file_path, item_name, 0))
        conn_sql.commit()

        # Adds to friend groups
        for each in fg_list:
            ins = 'INSERT INTO Share VALUES(%s,%s,%s)'
            cursor.execute(ins, (each, item_id, email))
            conn_sql.commit()
    else:
    	error = 'Not in Friend Group'
    	return render_template('sharePri.html',error = error)
    cursor.close()
    return redirect(url_for('home'))


# Friends
@app.route('/addFriend')
def addFriend():
    return render_template('addFriend.html')


@app.route('/addFriendAuth', methods=['GET', 'POST'])
def addFriendAuth():
    fg_name = request.form['fg_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    mem_email = request.form['mem_email']
    creator_email = session['email']

    cursor = conn_sql.cursor()
    # checks for exisiting friend group
    checkquery = "SELECT fg_name FROM FriendGroup WHERE fg_name = %s AND email = %s"
    cursor.execute(checkquery, (fg_name, creator_email))
    checkfg = cursor.fetchone()

    # checks for exisiting person
    checkquery = "SELECT first_name, last_name, email FROM Person WHERE first_name = %s " \
                 "AND last_name = %s AND email = %s"
    cursor.execute(checkquery, (first_name, last_name, mem_email))
    checkper = cursor.fetchone()

    if (checkfg is not None and checkper is not None):
        # checks if person is in friendgroup
        checkquery = "SELECT member_email FROM Belong WHERE member_email = %s " \
                     "AND creator_email = %s AND fg_name = %s"
        cursor.execute(checkquery, (mem_email, creator_email, fg_name))
        checkboth = cursor.fetchone()
        if (checkboth):
            error = "Friend is already in group!"
            cursor.close()
            return render_template('addFriend.html', error=error)
        else:
            ins = "INSERT INTO Belong VALUES (%s,%s,%s)"
            cursor.execute(ins, (mem_email, fg_name, creator_email))
            conn_sql.commit()
            cursor.close()
            flash("Friend has been added!")
            return render_template('addFriend.html')
    else:
        cursor.close()
        error = "Friend Group or Person does not exist!"
        return render_template('addFriend.html', error=error)


@app.route('/delFriend')
def delFriend():
    email = session['email']
    cursor = conn_sql.cursor()
    query = 'SELECT fg_name FROM FriendGroup WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchall()
    cursor.close()
    return render_template('delFriend.html', groups=data)

#Only owner can remove friend from Friend Group
@app.route('/delFriendAuth', methods=['GET', 'POST'])
def delfFriendAuth():
    email = session['email']
    their_email = request.form['mem_email']
    fg_name = request.form.get['fg_name']

    checkQ = 'SELECT member_email FROM Belong WHERE member_email = %s AND creator_email = %s AND fg_name = %s'
    delTag = 'DELETE FROM tag WHERE tagger = %s OR taggee = %s'
    delPost = 'DELETE FROM Share WHERE email = %s AND fg_name = %s'
    delQuery = 'DELETE FROM Belong WHERE member_email = %s AND creator_email = %s AND fg_name = %s'
    cursor = conn_sql.cursor()
    # check if their in fg
    cursor.execute(checkQ, (their_email, email, fg_name))
    data = cursor.fetchone()
    if data is None:
        error = 'Person is not in Friend Group or does not exist. Please try again!'
        return render_template('delFriend.html', error=error)

    # delete Tags
    cursor.execute(delTag, (their_email, their_email ))
    # delete Post
    cursor.execute(delPost, (email, fg_name))
    conn_sql.commit()
    # delete Person
    cursor.execute(delQuery, (their_email, fg_name, email))
    conn_sql.commit()

    cursor.close()
    return render_template('delFriend.html')

# Tags
@app.route('/manTags')
def manTags():
    email = session['email']
    cursor = conn_sql.cursor()
    query = 'SELECT tagger, item_id,tag_time FROM Tag WHERE tagged = %s AND status = 0'
    query2 = 'SELECT item_id FROM ContentItem NATURAL JOIN Share WHERE is_pub = 1 OR (Share.fg_name IN (SELECT fg_name FROM Belong WHERE email = %s))'
    cursor.execute(query, (email))
    data = cursor.fetchall()
    cursor.execute(query2, (email))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('manTags.html', tags=data, ids=data2)


@app.route('/tagAcc', methods=['GET', 'POST'])
def tagAcc():
    email = session['email']
    item_id = request.form.get('item_id')

    cursor = conn_sql.cursor();
    query = "UPDATE Tag SET status = %s WHERE tagged = %s AND item_id = %s"
    cursor.execute(query, (True, email, item_id))
    conn_sql.commit()
    cursor.close()
    return redirect(url_for('manTags'))


@app.route('/tagDec', methods=['GET', 'POST'])
def tagDecline():
    email = session['email']
    item_id = request.form.get('item_id')

    cursor = conn_sql.cursor()
    query = "DELETE FROM Tag WHERE tagged = %s AND item_id = %s"
    cursor.execute(query, (email, item_id))
    conn_sql.commit()
    cursor.close()
    return redirect(url_for('manTags'))


@app.route('/tagSome', methods=['GET', 'POST'])
def tagSome():
    x_email = session['email']
    y_email = request.form['y_email']
    item_id = request.form.get['item_id']

    cursor = conn_sql.cursor()
    # check if already tagged in same post by same person
    query = 'SELECT tagger,tagged, item_id, status FROM Tag WHERE tagger = %s AND tagged = %s AND item_id = %s'
    cursor.execute(query, (x_email, y_email, item_id))
    data = cursor.fetchone()
    # check if they can actually see post
    query2 = 'SELECT item_id FROM ContentItem NATURAL JOIN Share WHERE ContentItem.item_id = %s AND (is_pub = 1 OR Share.fg_name IN (SELECT fg_name FROM Belong WHERE email = %s))'
    cursor.execute(query2, (item_id, y_email))
    q2data = cursor.fetchone()
    # check if y exists
    crp = 'SELECT email FROM Person WHERE email = %s'
    cursor.execute(crp, (y_email))
    crpdata = cursor.fetchone()

    if data or not crp or not q2data:
        error = "You already tagged them in this post!"
        cursor.close()
        return render_template('manTags.html', error=error)

    else:
        if (x_email == y_email):
            status = 1
        else:
            status = 0
        ins = 'INSERT INTO Tag VALUES (%s,%s,%s,%s,None)'
        cursor.execute(item_id, x_email, y_email, status)
        conn_sql.commit()
        cursor.close()
        return redirect(url_for('manTags'))

#Friend Groups
@app.route('/viewFG')
def viewFG():
    email = session['email']

    cursor = conn_sql.cursor()
    query = 'SELECT fg_name,creator_email FROM Belong WHERE member_email = %s'

    cursor.execute(query, email)
    data = cursor.fetchall()
    
    cursor.close()
    return render_template('viewFG.html', data=data)

@app.route('/createFG')
def createFG():
	return render_template('createFG.html')

@app.route('/createFGAuth', methods = ['GET','POST'])
def createFGAuth():
	email = session['email']
	fg_name = request.form['fg_name']
	description = request.form['description']

	cursor = conn_sql.cursor()
	check = 'SELECT fg_name FROM FriendGroup WHERE fg_name = %s AND email = %s'
	cursor.execute(check,(fg_name,email))
	querycheck = cursor.fetchone()

	if(querycheck):
		error = "You already have a friend group under this name"
		return render_template('createFG.html', error = error)
	else:
		ins1 = 'INSERT INTO FriendGroup VALUES (%s,%s,%s)'
		ins2 = 'INSERT INTO Belong VALUES (%s, %s, %s)'
		cursor.execute(ins,(fg_name,description,email))
		conn_sql.commit()
		cursor.execute(ins2,(email,fg_name,email))

@app.route('/addComment')
def comment():
    # we are using rate as comment table
    return render_template('addComment.html')

app.secret_key = 'FDSJKGSEW'

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
