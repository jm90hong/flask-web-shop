from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

def init():
    print('초기화 작업')
    try:
        conn = sqlite3.connect('database.db')
        conn.execute('CREATE TABLE STUDENTS (NAME TEXTm ADDR TEXT, CITY TEXTm PIN TEXT)')
        conn.close()
    except:
        print('이미 db 생성됨')
        
@app.route('/test')
def hello_world():
    init()
    return 'Hello World!'

@app.route('/')
def hello():
    data = request.args
    print(data.get('name'))
    
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")



if __name__ == '__main__':
    app.run()