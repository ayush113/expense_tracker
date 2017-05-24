import sqlite3 #module to interact with DBMS which manages the program's data
import time #module which allows us to get real time
from datetime import datetime #module which allows us to verify user input for dates
import string
from tabulate import tabulate

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
        pick=cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM purchases")
        pick=cur.fetchall()
        db.commit()
      
except:
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS purchases")
        cur.execute("""CREATE TABLE users(userID INTEGER,
                                          userName TEXT,
                                          pwd TEXT,
                                          question TEXT,
                                          ans TEXT,
                                          budget REAL,
                                          PRIMARY KEY(userID))""")        
     
        cur.execute("""CREATE TABLE purchases(purchaseID INTEGER,
                                              desc TEXT,
                                              userID INTEGER,
                                              cat TEXT,
                                              loc TEXT,
                                              price REAL,
                                              day INT,
                                              month INT,
                                              year INT,
                                              PRIMARY KEY(purchaseID),
                                              FOREIGN KEY(userID) REFERENCES users(userID)
                                              ON UPDATE RESTRICT ON DELETE CASCADE)""")
        cur.execute("""CREATE TABLE years(month INTEGER,
                                          desc TEXT,
                                          PRIMARY KEY(month))""")
        db.commit()

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
                                        
class User(object):     #class for single user
    def __init__(self, userID, userName, pwd, question, ans, budget):
        self.userID=userID
        self.userName=userName
        self.pwd=pwd
        self.question=question
        self.ans=ans
        self.budget=budget

    def create(self): #stores user's details into database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO users(userName,pwd,question,ans,budget) VALUES (?,?,?,?,?)",(self.userName,self.pwd,self.question,self.ans,self.budget))
            db.commit()

    def edit(self):  #edits user's details and updates them in database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE users SET userName=?, pwd=?, question=?, ans=?, budget=? WHERE userID=?",(self.userName, self.pwd, self.question, self.ans, self.budget, self.userID))
            db.commit()
            
    def delete(self):  #deletes user account from database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM users WHERE userID = ?" ,(self.userID,))
            db.commit()
    
    def add_expense(self,values):   #adds expense with values (a list) and stores them in database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO purchases(userID, desc, cat, loc, day, month, year, price) VALUES (?,?,?,?,?,?)",
            (self.userID, values[0], values[1], values[2], values[4], values[5], values[6], values[3]))
            db.commit()
        print "\n\t\t\tEXPENSE ADDED!"

    def edit_expense(self,purchaseID,values):   #edits expense details and updates them in database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE purchases SET userID=?, desc=?, cat=?, loc=?, day=?, month=?, year=?, price=? WHERE purchaseID=?",(
            self.userID, values[0], values[1], values[2], values[4], values[5], values[6], values[3], purchaseID))
            db.commit()
        print "\n\t\t\tEXPENSE EDITED!"

    def delete_expense(self,purchaseID):    #deletes expense from database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM purchases WHERE purchaseID=?",(purchaseID,))
            db.commit()
        print "\n\t\t\tEXPENSE DELETED!"

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

client=User(0,'','','','',0.0) #global object of User class (will be used for login processes)

def begin():    #start menu
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
    except ValueError: #checks to see if 'choice' is a string
        print "\n\t\t\tERROR: INPUT NOT VALID!"
        begin()

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X    

def signup():   #menu for a customer to sign up for an account
    print "\n\t\tSIGN UP FOR AN ACCOUNT IN EXPENSE TRACKER 9000 XL!"

    userName=pwd=question=ans=''
    budget=-1
    while (len(userName)<5 or len(pwd)<6 or len(question)==0 or len(ans)==0 or budget<=0):
        print "\n\t\tUSERNAME MUST BE 5 CHARACTERS OR GREATER!\n\t\tPASSWORD MUST BE 6 CHARACTERS OR GREATER!"
        userName=raw_input("\n\t\tEnter your username - ")
        if (userName==''):
            print "\n\t\tRETURNING TO USER MENU..."
            enter()
        pwd=raw_input("\n\t\tEnter your password - ")
        if (pwd==''):
            print "\n\t\tRETURNING TO USER MENU..."
            enter()
        question=raw_input("\n\t\tEnter a security question to retrieve password - ")
        if (question==''):
            print "\n\t\tRETURNING TO USER MENU..."
            enter()
        ans=raw_input("\n\t\tEnter your answer to the security question - ")
        if (ans==''):
            print "\n\t\tRETURNING TO USER MENU..."
            enter()
        try:
            budget=raw_input("\n\t\tEnter your monthly budget - ") #ensures that budget is a float value
            if (budget==''):
                print "\n\t\tRETURNING TO USER MENU..."
                enter()
            budget=float(budget)
        except:
            continue
        
    with sqlite3.connect(db_name) as db:  #checks to see if username is taken
        cur=db.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE userName=?",(userName,))
        res=cur.fetchall()
        db.commit()
    if res[0][0]==1:
        print "\n\t\tUSERNAME ALREADY EXISTS! PLEASE RE-ENTER DETAILS!"
        signup()

    client.userName=userName    #updates global client details with that of user who just logged in
    client.pwd=pwd
    client.question=question
    client.ans=ans
    client.budget=budget
    client.create()

    print "\n\t\tTHANK YOU FOR CREATING AN ACCOUNT WITH US!\n\t    STAY UP-TO-DATE WITH YOUR FINANCES WITH EXPENSE TRACKER 9000 XL"
    begin()

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def login():    #login menu to ensure smooth login and to help user retrieve forgotten password
    print "\n\t\tLOGIN TO YOUR ACCOUNT!\n\t   (Forgot password? Enter 0 for all prompts)"

    userName=raw_input("\n\t\tEnter your username - ")
    pwd=raw_input("\n\t\tEnter your password - ")

    if (userName==pwd==''):
        print "\n\t\tRETURNING TO PREVIOUS MENU..."
        begin()
        
    elif (userName=='0' and pwd=='0'): #code block for forgotten password
        print "\n\t\tFORGOT PASSWORD? NO PROBLEM!"
        userName=raw_input("\n\t\tEnter your username - ")

        if (userName==''):
            print "\n\t\tRETURNING TO PREVIOUS MENU..."
            login()
            
        else:
            
            with sqlite3.connect(db_name) as db:
                cur=db.cursor()
                cur.execute("SELECT question, ans, pwd FROM users WHERE userName = ?",(userName,))
                res=cur.fetchall()
                db.commit()
                
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
            db.commit()
            
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

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
			
def create_expense(): #function that 'creates' the right expense details before sending them to User method 'add_expense'

    locs=[]
    cats=[]
    
    with sqlite3.connect(db_name) as db:
        
        cur=db.cursor()
        cur.execute("SELECT DISTINCT cat FROM purchases WHERE userID=?", (client.userID,))
        res=cur.fetchall()
        for (cat,) in res:
            cats.append(cat)
            
        cur.execute("SELECT DISTINCT loc FROM purchases WHERE userID=?", (client.userID,))
        res=cur.fetchall()
        for (loc,) in res:
            locs.append(loc)
            
    lists=[cats,locs]
    values=[]
    lists2=["category","location"]

    inp=raw_input("\n\t\tEnter a description of your purchase - ")
    if inp=='':
        print "\n\t\t\tRETURNING TO USER MENU..."
        enter()
    else:
        values.append(inp)
    
    for i in range(2):  #loop that iteratively stores data about location, category and description w/o rewriting code
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
                enter()
        elif inp=='':
            print "\n\t\t\tRETURNING TO USER MENU..."
            enter()
        else:
            values.append(inp)

    priceInp=raw_input("\n\t\tEnter the amount - ")
    try:
        price=float(priceInp)
    except TypeError:
        print "\n\t\t\tRETURNING TO USER MENU..."
        enter()
    else:
        if price>0:
            values.append(price)
        else:
            print "\n\t\tINVALID INPUT!"
            enter()

    dateInp=raw_input("\n\tEnter the date of purchase (Hit 1 for today's date to be entered) (DD/MM/YYYY) - ")
    if dateInp=='1':
        timeNow=time.localtime()    #gives the time right now in the form of tuple
        values.append(timeNow[2])
        values.append(timeNow[1])
        values.append(timeNow[0])
    elif dateInp=='':
        print "\n\t\t\tRETURNING TO USER MENU..."
        enter()
    else:
        try:
            day=int(dateInp[0:2])
            month=int(dateInp[3:5])
            year=int(dateInp[6:])
            timePurch=datetime(year,month,day)  #used to check if date entered by user is legit
        except:
            print "\n\t\tINVALID DATE!"
            enter()
        else:
            values.append(day)
            values.append(month)
            values.append(year)

    return values

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def choose_expense():

            #allows the user to pick an expense to edit/delete before sending that
            #expense's purchaseID to User method 'edit_expense'/'delete_expense'
    
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("SELECT purchaseID, desc, price, cat, loc, day||'-'||month||'-'||year from purchases WHERE userID=? ORDER BY year desc, month desc, day desc",(client.userID,))
        res=cur.fetchall()
        db.commit()
    if len(res)!=0:
        ids=[]
        for rec in res:
            ids.append(str(rec[0]))
        print tabulate(res, ["PurchaseID","Description","Price","Category","Location","Date(DD-MM-YYYY)"], tablefmt='grid')
        idInp=raw_input("\n\tEnter the ID of the expense - ")
        if idInp=='':
            print "\n\t\t\tRETURNING TO USER MENU..."
            enter()
        elif idInp in ids:
            return int(idInp)
        else:
            print "\n\tINVALID INPUT!"
            print "\n\t\t\tRETURNING TO USER MENU..."
            enter()            
    else:
        print "\n\tNO EXPENSES TO DISPLAY!"
        enter()

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
	
def details():

    #displays the monthly expenses, no. of purchases made in the current month, 
    #and total expenses in the current year; also displays the monthly budget

    todate=time.asctime().split()
    today=time.localtime()
    
    monthExpenses=0.0
    monthNo=0
    yearExpenses=0.0
    
    with sqlite3.connect(db_name) as db:
        
        cur=db.cursor()
        cur.execute("SELECT SUM(price) FROM purchases WHERE userID={0} AND year={1}".format(client.userID, today[0]))
        res=cur.fetchall()
        
        if res[0][0]!=None:
            yearExpenses=res[0][0]
        else:
            yearExpenses=0.0
            
        cur.execute("SELECT SUM(price), COUNT(PurchaseID) FROM purchases WHERE userID={0} AND year={1} AND month={2}".format(client.userID, today[0], today[1]))
        res=cur.fetchall()
        
        if res[0][1]!=0:
            monthExpenses=res[0][0]
            monthNo=res[0][1]   
        else:
            monthExpenses=0.0
            monthNo=0
            
        db.commit()
    print "\n\t\t\t\t  %s %s %s %s\n\n\t\t\tEXPENSES THIS MONTH: %.2f\n\t\t\tPURCHASES THIS MONTH: %d\n\t\t\tTOTAL EXPENSES THIS YEAR: %.2f\n\t\t\tMONTHLY BUDGET: %.2f" % (todate[0], todate[1], todate[2], todate[4], monthExpenses, monthNo, yearExpenses, client.budget)

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
    
def enter(): #menu for the user to do the following stuff
    print "\n\t\t\t\tWELCOME %s!" % client.userName
    details()
    print "\n\t\t\t1 --> ADD EXPENSE"
    print "\n\t\t\t2 --> EDIT EXPENSE"
    print "\n\t\t\t3 --> DELETE EXPENSE"
    print "\n\t\t\t4 --> VIEW TRANSACTIONS"
    print "\n\t\t\t5 --> EDIT ACCOUNT DETAILS"
    print "\n\t\t\t6 --> DELETE ACCOUNT"
    print "\n\t\t\t0 --> LOGOUT"

    choice=raw_input("\n\tEnter your choice - ")

    if choice=='1':
        values=create_expense()
        client.add_expense(values)
        enter()
        
    elif choice=='2':
        purchaseID=choose_expense()
        values=create_expense()
        client.edit_expense(purchaseID, values)
        enter()
        
    elif choice=='3':
        purchaseID=choose_expense()
        client.delete_expense(purchaseID)
        enter()
        
    elif choice=='5':
        
        userNameInp=client.userName
        pwdInp=client.pwd
        questionInp=client.question
        ansInp=client.ans

        print "\n\t\tIF YOU WANT A DETAIL TO REMAIN AS IS, HIT 1 FOR THAT DETAIL"
        userName=pwd=question=ans=''
        budget=-1
        while (len(userName)<5 or len(pwd)<6 or len(question)==0 or len(ans)==0 or budget<=0):
            print "\n\t\tUSERNAME MUST BE 5 CHARACTERS OR GREATER!\n\t\tPASSWORD MUST BE 6 CHARACTERS OR GREATER!"
            userName=raw_input("\n\t\tEnter your username - ")
            if (userName==''):
                print "\n\t\tRETURNING TO USER MENU..."
                enter()
            pwd=raw_input("\n\t\tEnter your password - ")
            if (pwd==''):
                print "\n\t\tRETURNING TO USER MENU..."
                enter()
            question=raw_input("\n\t\tEnter a security question to retrieve password - ")
            if (question==''):
                print "\n\t\tRETURNING TO USER MENU..."
                enter()
            ans=raw_input("\n\t\tEnter your answer to the security question - ")
            if (ans==''):
                print "\n\t\tRETURNING TO USER MENU..."
                enter()
            try:
                budget=raw_input("\n\t\tEnter your monthly budget - ")
                if (budget==''):
                    print "\n\t\tRETURNING TO USER MENU..."
                    enter()
                budget=float(budget)
            except:
                continue
            
        if userName=='1':
            userName=userNameInp
        if pwd=='1':
            pwd=pwdInp
        if question=='1':
            question==questionInp
        if ans=='1':
            ans=ansInp
        if budget==1:
            budget=budgetInp
            
        client.userName=userName  #once the account details are edited, global 'client' details are updated 
        client.pwd=pwd
        client.question=question
        client.ans=ans
        client.budget=budget
        client.edit()
        enter()

    elif choice=='6':
        choice=raw_input("\n\tARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT? ALL DATA WILL BE DELETED! (Y/N) - ")
        if choice=='' or choice.lower()=='n' or choice.lower()=="no":
            print "\n\tACCOUNT NOT DELETED! RETURNING TO USER MENU..."
            enter()
        elif choice.lower()=='y' or choice.lower()=='yes':
            print "\n\tACCOUNT DELETED! WE'RE SAD TO SEE YOU GO :("
            client.delete()
            client.userID=0     #upon logout or deletion of account, 'client' details are re-set to default values
            client.userName=''
            client.pwd=''
            client.question=''
            client.ans=''
            client.budget=0.0
        begin()

    elif choice=='0':
        print "\n\t\tLOGGING OUT OF ACCOUNT..."
        client.userID=0
        client.userName=''
        client.pwd=''
        client.question=''
        client.ans=''
        client.budget=0.0
        print "\n\t\tRETURNING TO START MENU..."
        begin()

    else:
        print "\n\t\tWRONG/INVALID CHOICE!"
        enter()

begin()
                        
#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
        
            
            
            
        
    
        
      
        
		
		
        
        

        
                
        
                    
        

                
    
            
        
        
    
            
            
            
            
        
            
        
    


    
    
        
        

                
            
            
        
