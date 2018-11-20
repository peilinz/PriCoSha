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
