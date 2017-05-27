import sqlite3
import matplotlib.pyplot as plt

def GetData_Cat(Uname):
    conn = sqlite3.connect("Accounts.db")
    cur = conn.cursor()
    cur.execute("SELECT userId from users WHERE Username = ? ",(Uname,))
    res = cur.fetchone()
    if(len(res) == 0):
        print ("Invalid Username entered\nTry again enter a valid username(press 1)\nQuit(press any key)")
        k =int(raw_input())
        if(k==1):
            GetData_Cat(Uname)
        else:
            return -1
    else:
        cur.execute("SELECT cat FROM purchases WHERE userID = ? ",(res[0],))
        d1 = cur.fetchall()
        d2 = dict()
        for i in range(len(d1)):
            cur.execute("SELECT sum(price) FROM purchases WHERE userID = ? AND cat = ? ",(res[0],d1[i][0],))
            req = cur.fetchone()
            d2[d1[i][0]] = req[0]
    return d2

def DrawPie(dictG):
    fig1, ax1 = plt.subplots()
    ax1.pie(dictG.values(),labels=dictG.keys(),autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax1.axis('equal')
    plt.show()


DrawPie(GetData_Cat("ayushkumar"))
