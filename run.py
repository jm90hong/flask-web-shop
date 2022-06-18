import datetime
from this import d
from flask import Flask, jsonify, render_template, request, session
import sqlite3
import hashlib
app = Flask(__name__)
app.secret_key = "sdkaofkoa12321"

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
        conn.execute('CREATE TABLE purchases (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT,customer_id INTEGER,item_id INTEGER,count INTEGER, complete_ny TEXT)')
        
        

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

@app.route('/users/<uname>')
def  history(uname):
    user_id = session['id']
    

    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute("SELECT COUNT(*) FROM purchases WHERE customer_id={ctid}".format(ctid=user_id))
    num = cur.fetchone()[0]
    conn.close()


    return render_template(
        "history.html",
        session = session,
        totalCount=num
    )




#====PAGE====
@app.route('/')
def home():
    init()
    data = request.args
    canLogin = data.get('canLogin')
    return render_template(
            "index.html",
            session = session,
            canLogin=canLogin
        )


@app.route('/purchase/<itemId>')
def purchase(itemId):
    #item id 에 해당하는 item 가져오기
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute("SELECT * FROM items WHERE id='{id}'".format(id=itemId))
    rows = cur.fetchall()
    conn.close()
    return render_template(
            "purchase.html",
            session=session,
            itemName=rows[0][1],
            itemId=rows[0][0]
        )




@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")





#====ajax====
@app.route('/complete/<itemid>')
def complete(itemid):
    print('==itemid')
    print(itemid)
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()

    #purchase에 해당 아이템이 있는지 조사
    cur.execute('''
            SELECT * FROM purchases
            WHERE item_id={itemid}
            '''
            .format(itemid=itemid)
        )
    rows = cur.fetchall()
    if(rows):
        #아이템이 있으면? => 배송 처리
        cur.execute('''
            UPDATE purchases
            SET 
                complete_ny='y'
            WHERE item_id={item_id}
            '''
            .format(item_id=itemid)
        )
        conn.commit()
        conn.close()
        return 'ok'
        
    else:
        #아이템이 없으면? => 배송 불가
        
        conn.commit()
        conn.close()
        return 'fail'
    
    
    
    
    


@app.route('/remove/<itemid>')
def remove(itemid):
    
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute('''
            DELETE FROM items
            WHERE id={id}
            '''
            .format(id=itemid)
        )
    conn.commit()
    conn.close()
    return 'ok'

@app.route('/add')
def add():
    data = request.args
    item_name = data.get('name')
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute('''
            INSERT INTO items
            (name)
            VALUES
            ('{itemName}')
            '''
            .format(itemName=item_name)
        )
    conn.commit()
    conn.close()
    return 'ok'

@app.route('/cancel/<purchaseId>')
def cancelPurchase(purchaseId):
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute('''
            DELETE FROM purchases
            WHERE id={id}
            '''
            .format(id=purchaseId)
        )
    conn.commit()
    conn.close()
    return 'ok'



@app.route('/purchase/addPurchase')
def addPurchase():
    data=request.args
    count = data.get('count')
    item_id = data.get('itemid')
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute('''
            INSERT INTO purchases (timestamp, customer_id,item_id,count,complete_ny) 
            VALUES 
            ('{timestamp}', {customer_id}, {item_id}, {count}, 'n')'''
            .format(
                timestamp=datetime.datetime.now(),
                customer_id=session['id'],
                item_id=item_id,
                count=count
                )
        )
    conn.commit()
    conn.close()
    return 'ok'

@app.route('/getPuchaseListByUser')
def getItemListByUser():

    user_id = session['id']
    

    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute('''
    SELECT * FROM purchases AS p
    INNER JOIN items AS i
    ON p.item_id = i.id
    WHERE customer_id={ctid}'''.format(ctid=user_id))
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)   


@app.route('/getItemList')
def getItemList():
    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)   
    

@app.route('/axlogin')
def axlogin():

    data = request.args
    name = data.get('name')
    pw = data.get('pw')

    conn = sqlite3.connect('data-dev.sqlite')
    cur=conn.cursor()
    cur.execute('''
    SELECT * FROM users WHERE username='{name}' AND password_hash='{pw}'
    '''
    .format(name=name, pw=getEncryptedString(pw))
    )
    rows = cur.fetchall()
    conn.close()
    if(rows):
        auth = rows[0][1]
        session['id']=rows[0][0]
        session['username']=rows[0][1]
        session['auth']="a" if rows[0][2] == 1 else "c"
        
       



        return 'ok'
    else:
        return "fail"  


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
   



@app.route('/auth/logout')
def logout():
    #session reset
    for key in list(session.keys()):
        session.pop(key)
    return 'ok'
   





if __name__ == '__main__':
    app.run()