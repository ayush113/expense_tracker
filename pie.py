""" REMOVED CHECKING FOR USERNAMES AS VALID EXISTING USERNAMES ARE SUPPLIED BY PROGRAM
FUNCTION MAY BE MODIFIED TO TAKE MONTH AS INPUT - REMOVE LINES 12 - 20, Add month as argument to GetData_Cat FUNCTION
SUGGESTION _
Replace Dict with list.
Note : Implementation with dict is easier

"""

import sqlite3
import matplotlib.pyplot as plt

def GetData_Cat(Uname):
    conn = sqlite3.connect("Accounts.db")
    cur = conn.cursor()
    cur.execute("SELECT userId from users WHERE Username = ? ",(Uname,))
    res = cur.fetchone()
    try:
        month = int(raw_input("Enter the Month number i.e. 1 for January, for februray and so on"))
    except:
        print("Invalid input")
        k =raw_input("Press 1 for trying again anyvother key to quit ")
        if(k=="1"):
            GetData_Cat(Uname)
        else:
            return -1
    cur.execute("SELECT cat FROM purchases WHERE userID = ? AND month = ? ",(res[0],month,))
    d1 = cur.fetchall()
    d2 = dict()
    for i in range(len(d1)):
        cur.execute("SELECT sum(price) FROM purchases WHERE userID = ? AND cat = ? AND month= ?",(res[0],d1[i][0],month,))
        req = cur.fetchone()
        d2[d1[i][0]] = req[0]
    fig1, ax1 = plt.subplots()
    ax1.pie(dict.values(d2),labels=dict.keys(d2),autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax1.axis('equal')
    plt.title("EXPENSES BY CATEGORY")
    plt.savefig("pie month-"+str(month)+".png")
    plt.show()
GetData_Cat("ayushkumar")
