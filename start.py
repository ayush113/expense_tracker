import sqlite3 #module to interact with DBMS which manages the program's data
import time #module which allows us to get real time
from datetime import datetime #module which allows us to verify user input for dates
import string

db_name="Accounts.db"

#ensures referential integrity (https://pythonschool.net/databases/referential-integrity/) 
with sqlite3.connect(db_name) as db: 
    cur=db.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    db.commit()

try:    #checks if tables exist; if not, creates them
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        cur.execute("SELECT COUNT(*) FROM purchases")
        cur.execute("SELECT COUNT(*) FROM cats")
        cur.execute("SELECT COUNT(*) FROM locs")
except:
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("""CREATE TABLE users(userID INTEGER,
                                          userName TEXT,
                                          pwd TEXT,
                                          question TEXT,
                                          ans TEXT,
                                          budget REAL,
                                          PRIMARY KEY(userID))""")
        
        cur.execute("""CREATE TABLE cats(catID INTEGER,
                                         desc TEXT,
                                         PRIMARY KEY(catID))""")
        
        cur.execute("""CREATE TABLE locs(locID INTEGER,
                                         desc TEXT,
                                         PRIMARY KEY(locID))""")
        
        cur.execute("""CREATE TABLE purchases(purchaseID INTEGER,
                                              desc TEXT,
                                              userID INTEGER,
                                              catID INTEGER,
                                              locID INTEGER,
                                              price REAL,
                                              PRIMARY KEY(purchaseID),
                                              FOREIGN KEY(userID) REFERENCES users(userID)
                                              ON UPDATE RESTRICT ON DELETE CASCADE,
                                              FOREIGN KEY(catID) REFERENCES cats(catID)
                                              ON UPDATE RESTRICT ON DELETE RESTRICT,
                                              FOREIGN KEY(locID) REFERENCES locs(locID)
                                              ON UPDATE RESTRICT ON DELETE RESTRICT)""")
        
        db.commit()
                                        
class Purchase(object): #class for single purchase
    def __init__(self,purchaseID,desc,price,locID,catID,date):
        self.purchaseID=purchaseID
        self.desc=desc
        self.price=price
        self.locID=locID
        self.catID=catID
        self.date=date

class User(object):     #class for single user
    def __init__(self, userID, userName, pwd, question, ans,budget):
        self.userID=userID
        self.userName=userName
        self.pwd=pwd
        self.question=question
        self.ans=ans
        self.budget=budget

    def create(self):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO users(userName,pwd,question,ans,budget) VALUES (?,?,?,?,?)",(self.userName,self.pwd,self.question,self.ans,self.budget))
            db.commit()

    def edit(self):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE users SET userName=?, pwd=?, question=?, ans=?, budget=? WHERE userID=?",(self.userName, self.pwd, self.question, self.ans, self.budget, self.userID))
            db.commit()
            
    def delete(self):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM users WHERE userID = ?" ,(self.userID,))
            db.commit()
    
    def insert_expense(self,purchase):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO purchases(userID, desc, catID, locID, date, price) VALUES (?,?,?,?,?,?)",(self.userID, purchase.desc, purchase.catID, purchase.locID, purchase.date, purchase.price))
            db.commit()

    def edit_expense(self, purchase):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE purchases SET userID=?, desc=?, catID=?, locID=?, date=?, price=? WHERE purchaseID=?",(self.userID, purchase.desc, purchase.catID, purchase.locID, purchase.date, purchase.price, purchase.purchaseID))
            db.commit()

    def delete_expense(self, purchase):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM purchases WHERE purchaseID=?",(purchase.purchaseID,))
            db.commit()

client=User(0,'','','','',0.0)

def begin():
    print "\n%sEXPENSE TRACKER XL 9000\n%s(Created by Ayush & Joshua)" % (' '*50,' '*49)
    print "\n\t\tTo return to the previous menu, hit <Enter> for all prompts" 
    print "\n\n%s1 --> Login\n%s2 --> Sign Up!\n%s0 --> Exit program" % (' '*50, ' '*50, ' '*50)

    choice=raw_input("\n\t\tEnter your choice - ")

    try:
        choice=int(choice)
        if choice==1:
            login()
        elif choice==2:
            signup()
        elif choice==0:
            print "\n\t\tEXITING...GOOD-BYE!"
            exit()
        else:
            print "\n\t\tERROR: WRONG CHOICE!"
            begin()
            
    except TypeError:
        print "\n\t\t\tERROR: INPUT NOT VALID!"
        begin()

def signup():
    print "\n\t\tSIGN UP FOR AN ACCOUNT IN EXPENSE TRACKER 9000 XL!"

    userName=pwd=question=ans=''
    budget=-1

    while (len(userName)<5 or len(pwd)<6 or len(question)==0 or len(ans)==0 or budget<=0):
        print "\n\t\tUSERNAME MUST BE 5 CHARACTERS OR GREATER!\n\t\tPASSWORD MUST BE 6 CHARACTERS OR GREATER!"
        userName=raw_input("\n\t\tEnter your username - ")
        pwd=raw_input("\n\t\tEnter your password - ")
        question=raw_input("\n\t\tEnter a security question to retrieve password - ")
        ans=raw_input("\n\t\tEnter your answer to the security question - ")
        if (userName==pwd==question==ans==''):
            print "\n\t\tRETURNING TO PREVIOUS MENU..."
            begin()
        try:
            budget=int(raw_input("\n\t\tEnter your monthly budget - "))
        except:
            continue
        
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE userName=?",(userName,))
        res=cur.fetchall()
    if res[0][0]==1:
        print "\n\t\tUSERNAME ALREADY EXISTS! PLEASE RE-ENTER DETAILS!"
        signup()

    client.userName=userName
    client.pwd=pwd
    client.question=question
    client.ans=ans
    client.budget=budget
    client.create()

    print "\n\t\tTHANK YOU FOR CREATING AN ACCOUNT WITH US!\n\t    STAY UP-TO-DATE WITH YOUR FINANCES WITH EXPENSE TRACKER 9000 XL"
    begin()

def login():
    print "\n\t\tLOGIN TO YOUR ACCOUNT!\n\t   (Forgot password? Enter 0 for all prompts)"

    userName=raw_input("\n\t\tEnter your username - ")
    pwd=raw_input("\n\t\tEnter your password - ")

    if (userName==pwd==''):
        print "\n\t\tRETURNING TO PREVIOUS MENU..."
        begin()
        
    elif (userName=='0' and pwd=='0'):
        userName=raw_input("\n\t\tEnter your username - ")

        if (userName==''):
            print "\n\t\tRETURNING TO PREVIOUS MENU..."
            login()
            
        else:
            
            with sqlite3.connect(db_name) as db:
                cur=db.cursor()
                cur.execute("SELECT question, ans, pwd FROM users WHERE userName = ?",(userName,))
                res=cur.fetchall()
                
            if res==[]:
                print "INVALID USERNAME! RETURNING TO LOGIN MENU..."
                login()
                    
            question=res[0][0]
            ans=res[0][1]
            pwd=res[0][2]
            
            print "\n\t\tSECURITY QUESTION: %s" % question
            _ans_=raw_input("\n\t\tEnter your answer to the security question - ")
            
            if _ans_=='':
                print "\n\t\tRETURNING TO PREVIOUS MENU..."
                login()
                
            elif _ans_==ans:
                print "\n\t\tPASSWORD FOR ACCOUNT WITH USERNAME %s IS: %s" % (userName,pwd)
                login()
                
            else:
                print "WRONG ANSWER! RETURNING TO LOGIN MENU..."
                login()
            
    else:
        
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("SELECT * FROM users WHERE userName = ? AND pwd = ?",(userName, pwd))
            res=cur.fetchall()
            
        if res==[]:
            print "\n\t\tINVALID USERNAME/PASSWORD! RETURNING TO LOGIN MENU..."
            login()
            
        else:
            client.userID=res[0][0]
            client.userName=res[0][1]
            client.pwd=res[0][2]
            client.question=res[0][3]
            client.ans=res[0][4]
            client.budget=res[0][5]
            enter()

def enter():
    print "\n\t\t\t\tWELCOME %s!" % client.userName
    print "\n\t\t\t1 --> ADD EXPENSE"
    print "\n\t\t\t2 --> EDIT EXPENSE"
    print "\n\t\t\t3 --> DELETE EXPENSE"
    print "\n\t\t\t4 --> VIEW TRANSACTIONS"
    print "\n\t\t\t5 --> SET BUDGET"
    print "\n\t\t\t6 --> CHANGE PASSWORD"
    print "\n\t\t\t7 --> DELETE ACCOUNT"
    print "\n\t\t\t0 --> LOGOUT"

    try:
        choice=raw_input("\n\t\tEnter your choice - ")
    except TypeError:
        print "\n\t\t\tERROR: INPUT NOT VALID!"
        enter()

    locs=[]
    cats=[]
    descs=[]
    
    with sqlite3.connect(db_name) as db:
        
        cur=db.cursor()
        cur.execute("SELECT DISTINCT desc FROM cats, purchases WHERE userID=? and purchases.catID==cats.catID", (client.userID,))
        res=cur.fetchall()
        for (cat,) in res:
            cats.append(cat)
            
        cur.execute("SELECT DISTINCT desc FROM locs, purchases WHERE userID=? and purchases.locID=locs.locID", (client.userID,))
        res=cur.fetchall()
        for (loc,) in res:
            locs.append(loc)
            
        cur.execute("SELECT DISTINCT desc FROM purchases WHERE userID=?", (client.userID,))
        res=cur.fetchall()
        for (desc,) in res:
            descs.append(desc)
            
    lists=[descs,cats,locs]
    values=[]
    lists2=["description","category","location"]
    if choice==1:
        for i in range(3):
            if len(lists[i])!=0:
                print "\n\t\t\t  %s:" % lists2[i].upper()
                for j in range(len(lists[i])):
                    print "\n\t\t\t%d --> %s" % (j+1,lists[i][j])
                print "\n\tEnter the %s of your purchase by entering a number or enter a new %s" % (lists2[i],lists2[i])
            inp=raw_input("\n\t\tEnter the %s - " % lists2[i])
            if inp.isdigit():
                if int(inp)-1 in range(len(lists[i])):
                    values.append(lists[i][int(inp)-1])
                else:
                    print "\n\t\t\tWRONG CHOICE!"
                    login()
            elif inp=='':
                print "\n\t\t\tRETURNING TO LOGIN MENU..."
                login()
            else:
                values.append(inp)

        priceInp=raw_input("\n\t\tEnter the amount - ")
        try:
            price=float(priceInp)
        except TypeError:
            print "\n\t\t\tRETURNING TO LOGIN MENU..."
            login()
        else:
            if price>0:
                values.append(price)
            else:
                print "\n\t\tINVALID INPUT!"
                login()

        dateInp=raw_input("\n\tEnter the date of purchase (Hit 1 for today's date to be entered) (DD/MM/YYYY) - ")
        if dateInp=='1':
            timeNow=time.localtime()
            values.append(str(timeNow[2])+str(timeNow[1])+str(timeNow[0]))
        elif dateInp='':
            print "\n\t\t\tRETURNING TO LOGIN MENU..."
            login()
        else:
            try:
                day=int(dateInp[0:2])
                month=int(dateInp[3:5])
                year=int(dateInp[6:])
                timePurch=datetime(year,month,day)
            except:
                print "\n\t\tINVALID DATE!"
                login()
            else:
                values.append(str(day)+"/"+str(month)+"/"+str(year))

        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute(

        purchaseID,desc,price,locID,catID,date
        purchase=Purchase(0,values[0],values[3],values[4]
        client.insert_expense(purchase)
        
        

        
                
        
                    
        

                
    
            
        
        
    
            
            
            
            
        
            
        
    


    
    
        
        

                
            
            
        
