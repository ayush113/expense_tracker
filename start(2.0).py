import sqlite3 #module to interact with DBMS which manages the program's data
from time import localtime,asctime #module which allows us to get real time
from datetime import datetime #module which allows us to verify user input for dates
import matplotlib.pyplot as plt #module which allows us to plot graphs and pie-charts
from tabulate import tabulate #module which allows us to tabulate purchases by user
from numpy import arange,linspace #module which helps matplotlib
import smtplib #module which sends reports and verification code to email address
from random import randint #used for verification of email address
from os import remove #used to delete files generate for reports
from os.path import basename #function that returns base path of file
from email import Encoders #module used to encode attachment
from email.mime.base import MIMEBase #MIMEBase object that allows us to send files of virtually any extension
from email.mime.multipart import MIMEMultipart #module which allows us to send attachments 
from email.mime.text import MIMEText #MIMEBase child class which caters specifically to text files

db_name="Accounts.db"
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
sendEmail="expense.trackerxl@gmail.com"
sendPwd="extrack9000"

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
                                          email TEXT,
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
    def __init__(self, userID, userName, pwd, question, ans, budget, email):
        self.userID=userID
        self.userName=userName
        self.pwd=pwd
        self.question=question
        self.ans=ans
        self.budget=budget
        self.email=email

    def create(self): #stores user's details into database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO users(userName,pwd,question,ans,budget,email) VALUES (?,?,?,?,?,?)",(self.userName,self.pwd,self.question,self.ans,self.budget,self.email))
            db.commit()

    def edit(self):  #edits user's details and updates them in database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE users SET userName=?, pwd=?, question=?, ans=?, budget=?, email=? WHERE userID=?",(self.userName, self.pwd, self.question, self.ans, self.budget, self.email, self.userID))
            db.commit()
            
    def delete(self):  #deletes user account from database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM users WHERE userID = ?" ,(self.userID,))
            db.commit()
    
    def add_expense(self,values):   #adds expense with values (a list) and stores them in database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO purchases(userID, desc, cat, loc, day, month, year, price) VALUES (?,?,?,?,?,?,?,?)",
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

client=User(0,'','','','',0.0,'') #global object of User class (will be used for login processes)

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def get_cats(): #returns list of categories of user
    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        cur.execute("SELECT DISTINCT cat FROM purchases WHERE userID=?",(client.userID,))
        res=cur.fetchone()
        cats=[]
        while res!=None:
            cats.append(res[0])
            res=cur.fetchone()
    return cats

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def month_stats(month, year): #matplotlib object that contains a pie chart and bar graph of monthly expenses
    
    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        
        cats=get_cats()
        
        mDict={}
        for cat in cats:
            mDict[cat]=0.0
            
        cur.execute("SELECT cat, SUM(price) FROM purchases WHERE userID=? and month=? and year=? GROUP BY cat",(client.userID, month, year))
        res=cur.fetchone()

        while res!=None:
            mDict[res[0]]=res[1]
            res=cur.fetchone()
            
    
    fig=plt.figure()
    
    ax1=fig.add_subplot(212)
    ax1.pie(mDict.values(), labels=mDict.keys(), shadow=True, startangle=90, labeldistance=-10)
    ax1.axis('equal')
    ax1.legend()
    
    ax2=fig.add_subplot(211)
    x_pos=arange(len(cats))
    ax2.bar(left=x_pos, height=mDict.values(), width=0.6, align='center')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(mDict.keys())
    ax2.set_title("%s-%d" % (months[month-1],year))
    ax2.set_ylabel('Rupees')

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def year_stats_all(year): #matplotlib object that contains a stacked bar graph of yearly expenses by category for every month and includes a table
    cats=get_cats()
    len_cats=len(cats)
    yList=[]
    catDict={}
    monthList=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for cat in cats:
        catDict[cat]=0.0
    for i in range(len_cats):
        yList.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        for i in range(len_cats):
            cur.execute("SELECT month, SUM(price) FROM purchases WHERE userID=? AND year=? AND cat=? GROUP BY month", (client.userID, year, cats[i]))
            res=cur.fetchone()
            while res!=None:
                yList[i][res[0]-1]=res[1]
                res=cur.fetchone()
    
    #plt.style.use('ggplot')
    colors=plt.cm.rainbow(linspace(0,0.4,len_cats))
    fig,ax1=plt.subplots()
    x_pos=arange(12)+0.5
    botList=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for i in range(len_cats):
        ax1.bar(left=x_pos,height=yList[i],width=0.6,align='center',bottom=botList,color=colors[i])
        for y in range(12):
            botList[y]+=yList[i][y]
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([])
    ax1.set_title(str(year))
    ax1.set_ylabel('Rupees')

    plt.table(cellText=yList,rowLabels=cats, rowColours=colors, colLabels=months, loc='bottom')
    plt.subplots_adjust(left=0.2, bottom=0.2)

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def year_stats_pies(year): #matplotlib object that contains yearly expenses by category and month in pie-charts
    cats=get_cats()
    len_cats=len(cats)
    yList=[]
    catDict={}
    monthList=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for cat in cats:
        catDict[cat]=0.0

    with sqlite3.connect("Accounts.db") as db:
        cur=db.cursor()
        cur.execute("SELECT month, SUM(price) FROM purchases WHERE userID=? AND year=? GROUP BY month",(client.userID,year))
        res=cur.fetchone()
        while res!=None:
            monthList[res[0]-1]=res[1]
            res=cur.fetchone()
        cur.execute("SELECT cat,SUM(price) FROM purchases WHERE userID=? GROUP BY cat",(client.userID,))
        res=cur.fetchone()
        while res!=None:
            catDict[res[0]]=res[1]
            res=cur.fetchone()

    fig=plt.figure()
    ax1=fig.add_subplot(121)
    ax1.pie(catDict.values(), labels=catDict.keys(), shadow=True, startangle=90, labeldistance=-10)
    ax1.axis('equal')
    ax1.legend()
    ax1.set_title(str(year))
    ax2=fig.add_subplot(122)
    ax2.pie(monthList, labels=months, shadow=True, startangle=90, labeldistance=-10)
    ax2.axis('equal')
    ax2.legend()
   

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

def validate_email(userName,email):  #validates the email address by sending a verification code

    randNo=randint(10000,99999)
    print "\n\tSENDING VERIFICATION EMAIL. ENSURE INTERNET CONNECTION AND CHECK YOUR MAIL!"
    message = "From: Expense Tracker 9000XL <expense.trackerxl@gmail.com>\nTo: %s <%s>\nMIME-Version: 1.0\nContent-type: text/html\nSubject: Email Verification\n<p>Dear %s,</p><p>\nBelow is the verification code for completion of registration on Expense Tracker 9000XL.</p><p>\nEnter the code in the program to complete registration.\n</p><h1><b>%d</b></h1>" % (userName, email, userName, randNo)
    try:
        smtpObj=smtplib.SMTP("smtp.gmail.com",587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(sendEmail,sendPwd)
        smtpObj.sendmail(sendEmail,email,message)
    except smtplib.SMTPException:
        return False

    code=raw_input("\n\tEnter the verification code - ")
    if code==str(randNo):
        print "\n\tVERIFICATION COMPLETED SUCCESSFULLY!"
        return True
    else:
        return False
        
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
            begin()
        pwd=raw_input("\n\t\tEnter your password - ")
        if (pwd==''):
            print "\n\t\tRETURNING TO USER MENU..."
            begin()
        question=raw_input("\n\t\tEnter a security question to retrieve password - ")
        if (question==''):
            print "\n\t\tRETURNING TO USER MENU..."
            begin()
        ans=raw_input("\n\t\tEnter your answer to the security question - ")
        if (ans==''):
            print "\n\t\tRETURNING TO USER MENU..."
            begin()
        try:
            budget=raw_input("\n\t\tEnter your monthly budget - ") #ensures that budget is a float value
            if (budget==''):
                print "\n\t\tRETURNING TO USER MENU..."
                begin()
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

    email=raw_input("\n\tEnter a valid email address for your account - ")
    if email=='':
        print "\n\t\tRETURNING TO USER MENU..."
        begin()
    if not validate_email(userName,email):
        print "\n\t\tCOULD NOT VALIDATE EMAIL ADDRESS! PLEASE RE-ENTER DETAILS!"
        signup() 

    client.userName=userName    #updates global client details with that of user who just logged in
    client.pwd=pwd
    client.question=question
    client.ans=ans
    client.budget=budget
    client.email=email
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
            client.email=res[0][6]
            enter()

#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
			
def create_expense(): #function that 'creates' the right expense details before sending them to User method 'add_expense'

    locs=[]
    cats=get_cats()
    
    with sqlite3.connect(db_name) as db:
        
        cur=db.cursor()   
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
    
    for i in range(2):  #loop that iteratively stores data about location and category w/o rewriting code
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
    except:
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
        timeNow=localtime()    #gives the time right now in the form of tuple
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

    todate=asctime().split()
    today=localtime()
    
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
    
def sendMail(subject, message, attachs):
    
    msg = MIMEMultipart()
    
    msg['Subject'] = subject
    msg['From'] = "Expense Tracker 9000XL <expense.trackerxl@gmail.com>"
    msg['To'] = "%s <%s>" % (client.userName, client.email)
    
    msg.attach(MIMEText(message))
    
    for attach in attachs:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                'attachment; filename="%s"' % basename(attach))
        msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()  #Sends an extended hello to server
        server.starttls() #starts ttls
        server.ehlo()  # sends hello
        server.login(sendEmail, sendPwd)  # FInd a way to store the password in a more secure way
        print "\n\t\tSENDING REPORT TO %s..." % (client.email,)
        server.sendmail(sendEmail, client.email, msg.as_string())
        server.close()
        print "\n\t\tSUCCESSFULLY SENT MAIL! PLEASE CHECK YOUR EMAIL!"
    except smtplib.SMTPException:
        print "\n\t\tUNABLE TO SEND MAIL! ENSURE INTERNET CONNECTION!"
    
#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
    
def enter(): #menu for the user to do the following stuff
    print "\n\t\t\t\tWELCOME %s!" % client.userName
    details()
    print "\n\t\t\t1 --> ADD EXPENSE"
    print "\n\t\t\t2 --> EDIT EXPENSE"
    print "\n\t\t\t3 --> DELETE EXPENSE"
    print "\n\t\t\t4 --> VIEW TRANSACTIONS"
    print "\n\t\t\t5 --> EMAIL MONTHLY REPORT"
    print "\n\t\t\t6 --> EMAIL YEARLY REPORT"
    print "\n\t\t\t7 --> EDIT ACCOUNT DETAILS"
    print "\n\t\t\t8 --> DELETE ACCOUNT"
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

    elif choice=='4':
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("SELECT desc, price, cat, loc, day||'-'||month||'-'||year from purchases WHERE userID=? ORDER BY year desc, month desc, day desc",(client.userID,))
            res=cur.fetchall()
            db.commit()
        if len(res)!=0:
            print tabulate(res, ["Description","Price","Category","Location","Date(DD-MM-YYYY)"], tablefmt='grid')
            today=localtime()
            month_stats(today[1],today[0])
            plt.show(block=False)
            year_stats_all(today[0])
            plt.show(block=False)
            year_stats_pies(today[0])
            plt.show()
            enter()
        else:
            print "\n\t\tNO EXPENSES TO DISPLAY!"
            enter()

    elif choice=='5':
        month=raw_input("\n\tEnter the month (1-12) - ")
        year=raw_input("\n\tEnter the year - ")
        if month.isdigit() and year.isdigit():
            month=int(month)
            year=int(year)
            with sqlite3.connect(db_name) as db:
                cur=db.cursor()
                cur.execute("SELECT COUNT(*), SUM(price) FROM purchases WHERE userID=? AND year=? AND month=?",(client.userID,year,month))
                res=cur.fetchone()
            if res[0]==0:
                print "\n\t\tNO EXPENSES INCURRED DURING THIS MONTH!"
            else:
                month_stats(month, year)
                plt.savefig("%s_%s-%d.png" % (client.userName,months[month-1],year))
                with sqlite3.connect(db_name) as db:
                    cur=db.cursor()
                    cur.execute("SELECT desc, price, cat, loc, day||'-'||month||'-'||year from purchases WHERE userID=? AND month=? AND year=? ORDER BY year desc, month desc, day desc",(client.userID, month, year))
                    result=cur.fetchall()
                fw=open("%s_%s-%d_Stats.txt" % (client.userName,months[month-1],year),"w")
                fw.write("\t\t%s-%d EXPENSES\n" % (months[month-1], year))
                fw.write(tabulate(result, ["Description","Price","Category","Location","Date(DD-MM-YYYY)"], tablefmt='grid'))
                fw.close()
                message="Dear %s,\nThis is your report for %s-%d.\n\n\t\tTOTAL EXPENSES INCURRED: %.2f rupees" % (client.userName, months[month-1], year, res[1])
                sendMail('%s-%d Monthly Report' % (months[month-1],year), message, ["%s_%s-%d.png" % (client.userName,months[month-1],year), "%s_%s-%d_Stats.txt" % (client.userName,months[month-1],year)])
                remove(basename("%s_%s-%d.png" % (client.userName,months[month-1],year)))
                remove(basename("%s_%s-%d_Stats.txt" % (client.userName,months[month-1],year)))
        else:
            print "\n\tINVALID MONTH AND/OR YEAR"
        enter()

    elif choice=='6':
        year=raw_input("\n\tEnter the year - ")
        if year.isdigit():
            year=int(year)
            with sqlite3.connect(db_name) as db:
                cur=db.cursor()
                cur.execute("SELECT COUNT(*), SUM(price) FROM purchases WHERE userID=? AND year=?",(client.userID,year))
                res=cur.fetchone()
            if res[0]==0:
                print "\n\t\tNO EXPENSES INCURRED DURING THIS YEAR"
            else:
                year_stats_all(year)
                plt.savefig("%s_%d_All.png" % (client.userName,year))
                year_stats_pies(year)
                plt.savefig("%s_%d_Pies.png" % (client.userName,year))
                with sqlite3.connect(db_name) as db:
                    cur=db.cursor()
                    cur.execute("SELECT desc, price, cat, loc, day||'-'||month||'-'||year from purchases WHERE userID=? AND year=? ORDER BY year desc, month desc, day desc",(client.userID, year))
                    result=cur.fetchall()
                fw=open("%s_%d_Stats.txt" % (client.userName,year),"w")
                fw.write("\t\t%d EXPENSES\n" % (year,))
                fw.write(tabulate(result, ["Description","Price","Category","Location","Date(DD-MM-YYYY)"], tablefmt='grid'))
                fw.close()
                message="Dear %s,\nThis is your report for %d.\n\n\t\tTOTAL EXPENSES INCURRED: %.2f rupees" % (client.userName, year, res[1])
                sendMail('%d Yearly Report' % (year,), message, ["%s_%d_All.png" % (client.userName, year), "%s_%d_Pies.png" % (client.userName,year), "%s_%d_Stats.txt" % (client.userName,year)])
                remove(basename("%s_%d_All.png" % (client.userName, year)))
                remove(basename("%s_%d_Pies.png" % (client.userName,year)))
                remove(basename("%s_%d_Stats.txt" % (client.userName,year)))
                
        else:
            print "\n\tINVALID MONTH AND/OR YEAR"
        enter()
            
    elif choice=='7':
        
        userNameInp=client.userName
        pwdInp=client.pwd
        questionInp=client.question
        ansInp=client.ans
        budgetInp=client.budget

        print "\n\t\tIF YOU WANT A DETAIL TO REMAIN AS IS, HIT 1 FOR THAT DETAIL"
        userName=pwd=question=ans=''
        budget=-1
        while ((len(userName)<5 and userName!='1') or (len(pwd)<6 and pwd!='1') or (len(question)==0 and question!='1') or (len(ans)==0 and ans!='1') or budget<=0):
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
            question=questionInp
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

    elif choice=='8':
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
            client.email=''
        begin()

    elif choice=='0':
        print "\n\t\tLOGGING OUT OF ACCOUNT..."
        client.userID=0
        client.userName=''
        client.pwd=''
        client.question=''
        client.ans=''
        client.budget=0.0
        client.email=''
        print "\n\t\tRETURNING TO START MENU..."
        begin()

    else:
        print "\n\t\tWRONG/INVALID CHOICE!"
        enter()

begin()
                        
#X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X
