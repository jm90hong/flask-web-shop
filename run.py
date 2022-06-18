from flask import Flask, jsonify, render_template, request
import sqlite3
import hashlib
app = Flask(__name__)


def getEncryptedString(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

def init():
    print('초기화 작업')

   
   
    try:
        conn = sqlite3.connect('data-dev.sqlite')

        #테이블 생성
        conn.execute('CREATE TABLE roles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        conn.execute('CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, role_id INTEGER, password_hash TEXT)')
        conn.execute('CREATE TABLE purchases (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,customer_id TEXT,item_id TEXT,count TEXT)')
        
        

        cur=conn.cursor()

        #items 기본 데이터 삽입
        cur.execute("INSERT INTO items (name) VALUES ('camera')")
        cur.execute("INSERT INTO items (name) VALUES ('eraser')")
        cur.execute("INSERT INTO items (name) VALUES ('pencil')")

        #role 기본 데이터 삽입
        cur.execute("INSERT INTO roles (name) VALUES ('admin')")  #->1
        cur.execute("INSERT INTO roles (name) VALUES ('customer')") #->2


        #users 기본 데이터 삽입
        users=[
            {
                'name':'admin',
                'password':getEncryptedString('yonsei'),
                'role_id':1
            },
            {
                'name':'c1',
                'password':getEncryptedString('C1'),
                'role_id':2
            },
            {
                'name':'c2',
                'password':getEncryptedString('C2'),
                'role_id':2
            },
        ]


        for user in users:
            cur.execute('''
                INSERT INTO users (username, role_id, password_hash) 
                VALUES 
                ('{username}','{role_id}', '{password_hash}')'''
                .format(username=user['name'], role_id=user['role_id'], password_hash=user['password'])
            )

        
        conn.commit()

    except Exception as e:
        print('DB exsist', e)
    finally:
        conn.close()
        
@app.route('/makedb')
def makedb():
    init()
    return 'SQLite DB has been made!'



#====페이지====
@app.route('/')
def home():
    init()
    data = request.args
    canLogin = data.get('canLogin')
    return render_template("index.html",canLogin=canLogin)





@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")

#====ajax====
@app.route('/getItemList')
def getItemList():
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/addUser')
def addUser():
    data=request.args
    name = data.get('name')
    pw = data.get('pw')
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    #기존 회원 검증
    cur.execute("SELECT * FROM users WHERE username='{name}'".format(name=name))
    rows = cur.fetchall()
    if(rows):
        conn.close()
        return 'ex'
    else:
        #기존 회원이 없으면 insert(가입)
        cur.execute('''
            INSERT INTO users (username, role_id, password_hash) 
            VALUES 
            ('{username}','2', '{password_hash}')'''
            .format(username=name, password_hash=getEncryptedString(pw))
        )
        conn.commit()
        conn.close()
        return 'ok'
   

   




if __name__ == '__main__':
    app.run()