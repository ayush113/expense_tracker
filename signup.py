import sqlite3

conn = sqlite3.connect('user.sqlite3')
cur=conn.cursor()

try:
    cur.execute('CREATE TABLE users (user_id TEXT, password TEXT,security_q TEXT,security_a TEXT)')
except:
    print "\n"


def start():
    user = dict()
    user["id"] = raw_input("Enter a username")
    user["password"] = raw_input("Enter your password")
    user["q"]=raw_input("SECURITY QUESTION")
    user["a"]=raw_input("YOUR ANSWER")

    cur.execute('INSERT INTO users (user_id,password,security_q,security_a) VALUES (?,?,?,?)',(user["id"],user["password"],user["q"],user["a"]))

#just a test
def cut():
    cur.execute('SELECT * FROM users')

    for row in cur:
        print row,"\n"
    
