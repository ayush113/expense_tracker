import Tkinter as Tk
import smtplib
from email import Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from time import localtime, sleep
from random import randint
import sqlite3
import tkMessageBox

sendEmail = "expense.trackerxl@gmail.com"
sendPwd = "extrack9000"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


########################################################################################################################
#                                       CLASS FOR USERS                                                                #
########################################################################################################################


class User(object):
    def __init__(self, user_id=0, name="", pwd="", budget=0.0, email="", cats=[], locs=[]):
        self.user_id = user_id
        self.name = name
        self.pwd = pwd
        self.budget = budget
        self.email = email
        self.cats = cats
        self.locs = locs

    def create(self):  # STORES USER'S DETAILS INTO DATABASE
        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO users(name, pwd, budget, email) VALUES (?,?,?,?,?,?)",
                        (self.name, self.pwd, self.budget, self.email))
            db.commit()

    def edit(self):  # EDITS USER'S DETAILS AND UPDATES THEM IN DATABASE
        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("UPDATE users SET userName=?, pwd=?, budget=?, email=? WHERE userID=?",
                        (self.name, self.pwd, self.budget, self.email, self.user_id))
            db.commit()

    def delete(self):  # DELETES USER ACCOUNT FROM DATABASE
        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("DELETE FROM users WHERE userID = ?", (self.user_id,))
            db.commit()

    def clear(self):  # CLEARS ALL MEMBER DATA
        self.user_id = 0
        self.name = ""
        self.pwd = ""
        self.budget = 0.0
        self.email = ""

########################################################################################################################
#                                       CLASS FOR PURCHASES                                                            #
########################################################################################################################


class Purchase(object):

    def __init__(self, user_id=0, purchase_id=0, dscr="", cat="", loc="", day=0, month=0, year=0, price=0.0):
        self.user_id = user_id
        self.purchase_id = purchase_id
        self.dscr = dscr
        self.cat = cat
        self.loc = loc
        self.day = day
        self.month = month
        self.year = year
        self.price = price

    def add_expense(self):  # ADDS EXPENSE WITH PURCHASE (DICTIONARY) TO DATABASE
        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO purchases(userID, dscr, cat, loc, day, month, year, price) "
                        "VALUES (?,?,?,?,?,?,?,?)",
                        (self.user_id, self.dscr, self.cat, self.loc,
                         self.day, self.month, self.year,
                         self.price))
            db.commit()

    def edit_expense(self, purchase):  # EDITS EXPENSE WITH PURCHASE (DICTIONARY) AND UPDATES TO DATABASE
        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("UPDATE purchases SET userID=?, dscr=?, cat=?, loc=?, day=?, month=?, year=?, price=? "
                        "WHERE purchaseID=?",
                        (self.user_id, self.dscr, self.cat, self.loc,
                         self.day, self.month, self.year,
                         self.price, self.purchase_id))
            db.commit()

    def delete_expense(self):  # DELETES EXPENSE FROM DATABASE
        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("DELETE FROM purchases WHERE purchaseID=?", (self.purchase_id,))
            db.commit()

user = User()
purchase = Purchase()

def send_mail(subject, message, attachs, rec_name=user.name, rec_email=user.email):

    # SENDS VERIFICATION EMAIL, PASSWORD SEND EMAIL, AND REPORTS TO USERS

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = "Expense Tracker 9000XL <expense.trackerxl@gmail.com>"
    msg['To'] = "%s <%s>" % (rec_name, rec_email)

    msg.attach(MIMEText(message, "html"))

    for attach in attachs:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % basename(attach))
        msg.attach(part)

    try:
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.ehlo()  # CONNECTS WITH HOST
        smtp_obj.starttls()  # TLS --> TRANSPORT LAYER SECURITY
        smtp_obj.ehlo()
        smtp_obj.login(sendEmail, sendPwd)
        smtp_obj.sendmail(sendEmail, rec_email, msg.as_string())
        smtp_obj.close()
        return True  # YAY! MAIL IS SENT!
    except smtplib.SMTPException:
        return False  # NOOO! MAIL IS NOT SENT!

########################################################################################################################
#                                       CLASS INTERFACE FOR START-UP WINDOW                                            #
########################################################################################################################

class StartWin(Tk.Frame):

    def __init__(self, master):

        ##########################
        # SETTING UP THE WIDGETS #
        ##########################

        Tk.Frame.__init__(self, master, bg="#21618c")
        self.master.title("START")
        self.introLabel = Tk.Label(self, text="WELCOME TO EXPENSE TRACKER 9000XL!",
                                   anchor=Tk.CENTER,
                                   font=('Britannic Bold', 30),
                                   fg="#f4d03f", bg="#21618c")
        self.loginBn = Tk.Button(self, text="LOGIN!",
                                 command=lambda: loginWin.tkraise(),
                                 anchor=Tk.CENTER,
                                 font=('Calibri', 20),
                                 fg="#f4d03f", bg="#424949",
                                 activebackground="#797d7f")
        self.signBn = Tk.Button(self, text="SIGN UP!",
                                command=lambda: signupWin.tkraise(),
                                anchor=Tk.CENTER,
                                font=('Calibri', 20),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f")
        self.quitBn = Tk.Button(self, text="QUIT!",
                                command=self.master.destroy,
                                anchor=Tk.CENTER,
                                font=('Calibri',20),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f")

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(30):
            self.rowconfigure(row, weight=1)
        for col in range(30):
            self.columnconfigure(col, weight=1)

        ##########################
        # DISPLAYING ON WINDOW   #
        ##########################

        self.introLabel.grid(row=2, column=5, rowspan=3, columnspan=20, sticky="news")
        self.loginBn.grid(row=8, column=13, rowspan=3, columnspan=5, sticky="news")
        self.signBn.grid(row=15, column=13, rowspan=3, columnspan=5, sticky="news")
        self.quitBn.grid(row=22, column=13, rowspan=3, columnspan=5, sticky="news")

    ####################
    #  CLASS METHODS   #
    ####################

    def reset(self):
        self.master.title("START")
        statBar.configure(text="Currently not signed in!", relief=Tk.SUNKEN, bg="black")

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)

def update_loc_cat():

    with sqlite3.connect(database) as db:
        cur = db.cursor()
        cur.execute("SELECT DISTINCT cat FROM purchases WHERE userID=?", (user.user_id,))
        res_cat = cur.fetchall()
        cur.execute("SELECT DISTINCT loc FROM purchases WHERE userID=?", (user.user_id,))
        res_loc = cur.fetchall()
    user.cats = []
    user.locs = []
    for (cat,) in res_cat:
        user.cats.append(cat)
    for (loc,) in res_loc:
        user.locs.append(loc)

########################################################################################################################
#                                       CLASS INTERFACE FOR LOGIN WINDOW                                               #
########################################################################################################################


class LoginWin(Tk.Frame):

    ##########################
    # SETTING UP THE WIDGETS #
    ##########################

    def __init__(self, master):
        Tk.Frame.__init__(self, master, bg="#21618c")

        self.master.title("LOGIN...")

        self.label = Tk.Label(self, text="LOGIN TO YOUR ACCOUNT!",
                              anchor=Tk.CENTER,
                              font=('Britannic Bold', 35),
                              fg="#f4d03f", bg="#21618c")

        self.userLabel = Tk.Label(self, text="Enter your username",
                                  anchor=Tk.CENTER,
                                  font=('Calibri', 18),
                                  fg="#f4d03f", bg="#21618c")

        self.pwdLabel = Tk.Label(self, text="Enter your password",
                                 anchor=Tk.CENTER,
                                 font=('Calibri', 18),
                                 fg="#f4d03f", bg="#21618c")

        self.userEntry = Tk.Entry(self,
                                  font=('Calibri', 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)

        self.pwdEntry = Tk.Entry(self,
                                 show="*",
                                 font=('Calibri', 18),
                                 fg="#000000",
                                 justify=Tk.LEFT,
                                 relief=Tk.SUNKEN,
                                 bd=3)

        self.loginBn = Tk.Button(self,
                                 text="Login!",
                                 font=('Calibri', 18),
                                 fg="#f4d03f", bg="#424949",
                                 activebackground="#797d7f",
                                 command=self.login)

        self.forgotBn = Tk.Button(self,
                                  text="Forgot Password?",
                                  font=('Calibri', 18),
                                  fg="#f4d03f", bg="#424949",
                                  activebackground="#797d7f",
                                  command=self.forgot)

        self.backBn = Tk.Button(self,
                                text="Back",
                                font=('Calibri', 18),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f",
                                command=lambda: startWin.tkraise())

        self.remVar = Tk.IntVar()
        self.remBn = Tk.Checkbutton(self,
                                    variable=self.remVar,
                                    font=('Calibri', 18),
                                    fg="#f4d03f", bg="#21618c",
                                    text="Remember Me",
                                    relief=Tk.FLAT,
                                    selectcolor="black",
                                    activebackground="#21618c",
                                    anchor=Tk.CENTER)

        self.submitBn = Tk.Button(self,
                                  font=('Calibri', 18),
                                  fg="#21618c", bg="#21618c",
                                  activebackground="#797d7f",
                                  command=self.submit,
                                  state=Tk.DISABLED,
                                  relief=Tk.FLAT)

        self.forgotFlag = 0
        self.forgotLabel = Tk.Label(self, text="",
                                    anchor=Tk.CENTER,
                                    font=('Calibri', 18),
                                    fg="#f4d03f", bg="#21618c")
        self.forgotEntry = Tk.Entry(self,
                                    font=('Calibri', 18),
                                    fg="black",
                                    justify=Tk.LEFT,
                                    disabledbackground="#21618c",
                                    state=Tk.DISABLED,
                                    relief=Tk.FLAT,
                                    bd=3, width=30)
        self.showLabel = Tk.Label(self, text="Show",
                                  anchor=Tk.CENTER,
                                  font=("Calibri",18),
                                  fg="#f4d03f", bg="#424949",
                                  relief=Tk.FLAT)

        self.showLabel.bind("<Motion>", lambda x: self.pwdEntry.configure(show=""))
        self.showLabel.bind("<Leave>", lambda x: self.pwdEntry.configure(show="*"))

        # self.master.bind_class("Text", "<Control-a>", self.selectall)
        # self.userEntry.bind("<Control-A>", self.selectall())

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(40):
            self.rowconfigure(row, weight=1)
        for col in range(20):
            self.columnconfigure(col, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        self.label.grid(row=3, column=6, rowspan=2, columnspan=9, sticky="news")
        self.userLabel.grid(row=8, column=6, rowspan=2, columnspan=4, sticky="news")
        self.userEntry.grid(row=8, column=11, rowspan=2, columnspan=2, sticky="news")
        self.pwdLabel.grid(row=12, column=6, rowspan=2, columnspan=4, sticky="news")
        self.pwdEntry.grid(row=12, column=11, rowspan=2, columnspan=1, sticky="news")
        self.loginBn.grid(row=18, column=8, rowspan=2, columnspan=3, sticky="news")
        self.remBn.grid(row=18, column=11, rowspan=2, columnspan=3, sticky="news")
        self.forgotBn.grid(row=24, column=9, rowspan=2, columnspan=3, sticky="news")
        self.backBn.grid(row=37, column=17, rowspan=2, columnspan=2, sticky="news")
        self.forgotEntry.grid(row=31, column=11, rowspan=2, columnspan=2, sticky="news")
        self.submitBn.grid(row=35, column=9, rowspan=2, columnspan=3, sticky="news")
        self.forgotLabel.grid(row=31, column=6, rowspan=2, columnspan=4, sticky="news")
        self.showLabel.grid(row=12, column=12, rowspan=2, sticky="news")

    ####################
    #  CLASS METHODS   #
    ####################

    # def selectall(self):
    #    self.userEntry.select_range(0, Tk.END)
    #    return "break"

    def reset(self):

        ####################
        # INITIAL SETTINGS #
        ####################
        self.userEntry.delete(0, Tk.END)
        self.pwdEntry.delete(0, Tk.END)
        self.master.title("LOGIN...")
        self.remVar.set(0)
        self.remBn.deselect()
        self.forgotFlag = 0
        statBar.configure(bg="black", relief=Tk.SUNKEN, text="Currently not signed in")
        self.forgotEntry.delete(0, Tk.END)
        self.forgotEntry.configure(state=Tk.DISABLED, relief=Tk.FLAT)
        self.submitBn.configure(text="", bg="#21618c", state=Tk.DISABLED, relief=Tk.FLAT)
        self.forgotLabel.configure(text="")

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)

    def forgot(self):
        if self.forgotFlag == 1:
            self.reset()
        else:
            self.forgotFlag = 1
            self.forgotLabel.configure(text="Enter email address")
            self.forgotEntry.configure(state=Tk.NORMAL, relief=Tk.SUNKEN, text="Enter email address")
            self.submitBn.configure(state=Tk.NORMAL, fg="#f4d03f", bg="#424949", relief=Tk.RAISED, text="Send Password")

    def login(self):

        name = self.userEntry.get()
        pwd = self.pwdEntry.get()

        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("SELECT userID, userName, pwd, budget, email FROM users WHERE "
                        "userName=? AND pwd=?", (name, pwd))
            res = cur.fetchone()

        if res is None:  # CHECKS IF USERNAME AND PASSWORD IS VALID
            statBar.bell()
            statBar.configure(bg="red", relief=Tk.RAISED, text="ERROR: USERNAME AND/OR PASSWORD IS INVALID!")
        else:
            user.user_id = res[0]
            user.name = res[1]
            user.pwd = res[2]
            user.budget = res[3]
            user.email = res[4]

            update_loc_cat()

            if self.remVar.get() == 1:
                file_obj = open("remember_me.txt", "w")
                file_obj.write(str(user.user_id))
                file_obj.close()

            userWin.reset()
            userWin.tkraise()

    def submit(self):

        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("SELECT userName, pwd FROM users WHERE email=?", (self.forgotEntry.get(),))
            res = cur.fetchone()

        if res is None:
            statBar.bell()
            statBar.configure(bg="red", relief=Tk.RAISED, text="ERROR: EMAIL NOT FOUND!")
        else:
            message = "<p>Dear %s</p><p>You have requested your password to be sent to your email. " \
                      "Below is your password; please store it carefully for future reference</p>" \
                      "<h1><b>%s</b></h1>" % (res[0], res[1])
            subject = "Forgot Password"
            if send_mail(subject, message, [], res[0], self.forgotEntry.get()):
                statBar.configure(bg="black", relief=Tk.SUNKEN, text="MAIL SUCCESSFULLY SENT!")
            else:
                statBar.bell()
                statBar.configure(bg="red", relief=Tk.RAISED, text="ERROR: INTERNET CONNECTION NOT ESTABLISHED!")

########################################################################################################################
#                                       CLASS INTERFACE FOR SIGNUP WINDOW                                              #
########################################################################################################################

class SignupWin(Tk.Frame):

    def __init__(self, master):

        Tk.Frame.__init__(self, master, bg="#21618c")

        ##########################
        # SETTING UP THE WIDGETS #
        ##########################

        self.master.title("SIGN UP")

        self.label = Tk.Label(self, text="CREATE A NEW ACCOUNT!",
                              anchor=Tk.CENTER,
                              font=("Britannic Bold", 35),
                              fg="#f4d03f",bg="#21618c")

        self.unameLabel = Tk.Label(self, text="Enter a Username (minimum 5 characters)",
                                   anchor=Tk.W,
                                   font=("Calibri", 18),
                                   fg="#f4d03f",bg="#21618c")

        self.plabel = Tk.Label(self, text="Enter a Password (minimum 6 characters)",
                               anchor=Tk.W,
                               font=("Calibri", 18),
                               fg="#f4d03f", bg="#21618c")

        self.plabelConf = Tk.Label(self, text = "Confirm the Password",
                                   anchor=Tk.W,
                                   font=("Calibri", 18),
                                   fg="#f4d03f", bg="#21618c")

        self.email_label = Tk.Label(self, text = "Enter a Valid Email Address",
                                    anchor=Tk.W,
                                    font=("Calibri", 18),
                                    fg="#f4d03f", bg="#21618c")

        self.enterUname = Tk.Entry(self, font=("Calibri", 18),
                                   fg="#000000",
                                   justify=Tk.LEFT,
                                   relief=Tk.SUNKEN,
                                   bd=3)

        self.enterpass = Tk.Entry(self, show="*",
                                  font=("Calibri", 18),
                                  fg="#000000", justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)

        self.enterpass2 = Tk.Entry(self, show="*",
                                   font=("Calibri", 18),
                                   fg="#000000", justify=Tk.LEFT,
                                   relief=Tk.SUNKEN,
                                   bd=3)

        self.enterEmail = Tk.Entry(self, font=("Calibri", 18),
                                   fg="#000000",
                                   justify=Tk.LEFT,
                                   relief=Tk.SUNKEN,
                                   bd=3)

        self.signupBn = Tk.Button(self, text="Submit",
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#424949",
                                  activebackground="#797d7f",
                                  command=self.submit)

        self.backBn = Tk.Button(self, text="Back",
                                font=("Calibri", 18),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f",
                                command=lambda: startWin.tkraise())

        self.showLabel = Tk.Label(self, text="Show",
                                  anchor=Tk.CENTER,
                                  font=("Calibri", 18),
                                  fg="#f4d03f",
                                  bg="#424949",
                                  relief=Tk.FLAT)

        self.showLabel.bind("<Motion>", self.show_pwd)
        self.showLabel.bind("<Leave>", self.hide_pwd)

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(17):
            self.rowconfigure(row, weight=1)
        for col in range(10):
            self.columnconfigure(col, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        self.label.grid(row=1, column=3, columnspan=4, sticky="news")
        self.unameLabel.grid(row=4, column=3, sticky="news")
        self.email_label.grid(row=6, column=3, sticky="news")
        self.plabel.grid(row=8, column=3, sticky="news")
        self.plabelConf.grid(row=10, column=3, sticky="news")
        self.signupBn.grid(row=13, column=4, sticky="news")
        self.backBn.grid(row=15, column=6, sticky="news")
        self.enterUname.grid(row=4, column=5, columnspan=2, sticky="news")
        self.enterEmail.grid(row=6, column=5, columnspan=2, sticky="news")
        self.enterpass.grid(row=8, column=5, sticky="news")
        self.enterpass2.grid(row=10, column=5, columnspan=2, sticky="news")
        self.showLabel.grid(row=8, column=6, sticky="news")

        ####  COPYING JOSH IS FUN ####
        ####     CLASS METHODS    ####


    def show_pwd(self, event=None):
        self.enterpass.configure(show="")
        self.enterpass2.configure(show="")

    def hide_pwd(self, event=None):
        self.enterpass.configure(show="*")
        self.enterpass2.configure(show="*")

    def submit(self):
        statBar.configure(bg="black", relief=Tk.SUNKEN, text="New User Details")
        errorFlag = 0
        uname = self.enterUname.get()
        email = self.enterEmail.get()
        pwd = self.enterpass.get()
        pwdConf = self.enterpass2.get()

        ###VARIOUS CHECKS TO ENSURE VALID INPUTS####

        if(len(pwd) < 6):
            statBar.bell()
            statBar.configure(bg="red",relief=Tk.RAISED,text="PASSWORD MUST BE AT LEAST 6 CHARACTERS LONG,RE-ENTER PASSWORD ")
            self.enterpass.delete(0, Tk.END)
            self.enterpass2.delete(0, Tk.END)
            errorFlag=1
        if(len(uname)<5):
            statBar.bell()
            statBar.configure(bg="red",relief=Tk.RAISED,text="USERNAME MUST BE AT LEAST 5 CHARACTERS LONG, ENTER VALID USERNAME")
            self.enterUname.delete(0,Tk.END)
            errorFlag=1
        if(len(email)==0):
            statBar.bell()
            statBar.configure(bg="red",relief=Tk.RAISED,text="EMAIL ID CAN NOT BE EMPTY")
            errorFlag=1
        else:
            stud = email.split("@")
            if (len(stud)!=2):
                statBar.bell()
                statBar.configure(bg="red",relief=Tk.RAISED,text="INVALID EMAIL ADRESS, ENTER VALID EMAIL ID")
                self.enterEmail.delete(0,Tk.END)
                errorFlag = 1
        if(pwd != pwdConf):
            statBar.bell()
            statBar.configure(bg="red",relief=Tk.RAISED,text="PASSWORDS DO NOT MATCH, RE-ENTER PASSWORD")
            errorFlag=1
            self.enterpass.delete(0,Tk.END)
            self.enterpass2.delete(0,Tk.END)

        #####   CHECKING HERE AFTER ENSURING ABOVE TO SAVE USER DATA USAGE   #####
        ##### THE PROGRAM NOW CHECKS IF THE USERNAME AND EMAIL ARE UNIQUE    #####

        if(errorFlag==0):
            statBar.configure(bg="green",relief=Tk.RAISED,text="CREATING USER ACCOUNT")
            with sqlite3.connect(database) as db:
                cur = db.cursor()
                cur.execute("SELECT COUNT(*) from users WHERE userName=?", (uname,))
                res = cur.fetchone()
                cur.execute("SELECT COUNT(*) from users WHERE email=?", (email,))
                resE = cur.fetchone()

            if res[0] == 1:
                errorFlag = 1
            if resE[0] == 1:
                errorFlag = 2

            if errorFlag == 1:
                statBar.bell()
                statBar.configure(bg="red", relief=Tk.RAISED, text="USERNAME ALREADY EXISTS, ENTER A DIFFERENT USERNAME")
                self.enterUname.delete(0,Tk.END)
            if errorFlag == 2:
                statBar.bell()
                statBar.configure(bg="red", relief=Tk.RAISED, text="EMAIL-ID ALREADY IN USE FOR ANOTHER USER, ENTER A DIFFERENT EMAIL-ID")
                self.enterEmail.delete(0, Tk.END)
            if errorFlag == 0:
                veriFlag = self.validate_email(uname,email)
                if(veriFlag!=1):
                    statBar.configure(bg="green",relief=Tk.RAISED,text="A VERIFICATION CODE HAS BEEN SENT TO YOUR INBOX")
                    self.checkEmail(veriFlag)
                else:
                    statBar.configure(bg="red",relief=Tk.RAISED,text="CAN NOT VERIFY EMAIL ID AT THE MOMENT, CHECK YOUR CONNECTION AND TRY AGAIN")


    ### DOES THE ACTUAL REGISTERING AFTER ENSURING EVERYTHING'S RIGHT ####

    def registerUser(self):
        u = self.enterUname.get()
        p = self.enterpass.get()
        e = self.enterEmail.get()
        with sqlite3.connect(database) as db:
            try:
                cur = db.cursor()
                cur.execute("INSERT INTO users (username,pwd,email) VALUES (?,?,?)",(u,p,e,))
                statBar.configure(bg="green",relief=Tk.SUNKEN,text="ACCOUNT CONFIGURED! PLEASE GO BACK TO LOG IN")
            except:
                statBar.bell()
                statBar.configure(bg="red",relief=Tk.RAISED,text="CONNECTION PROBLEM, TRY AGAIN!")

    ##### Don't even ask why I have done what I have done.

    def checkEmail(self,veriCode):
        global child
        child = Tk.Tk()
        label = Tk.Label(child,text="Enter the verification Code",relief=Tk.RAISED,justify=Tk.CENTER)
        global enterCode
        enterCode = Tk.Entry(child,relief=Tk.SUNKEN,justify=Tk.CENTER)
        changeDetails = Tk.Button(child,text="CHANGE DETAILS",relief=Tk.SUNKEN,anchor=Tk.E,command = lambda : child.destroy())
        subButton = Tk.Button(child,text="SUBMIT",relief=Tk.RAISED,anchor=Tk.E,command = lambda : self.verify(veriCode))
        label.pack()
        enterCode.pack()
        subButton.pack()
        changeDetails.pack()
        child.mainloop()

    def verify(self,veriCode):
            code = enterCode.get()
            if(code == str(veriCode)):
                tkMessageBox.showinfo("VERIFICATION","Your Email ID has been successfully verified")
                child.destroy()
                self.registerUser()
            else:
                tkMessageBox.showinfo("VERIFICATION","Sorry, the codes don't match try again")
                enterCode.delete(0,Tk.END)

    def reset(self):
        self.master.title("SIGN UP")
        statBar.configure(bg="black", text="Currently not signed in!", relief=Tk.SUNKEN)
        self.enterUname.delete(0, Tk.END)
        self.enterEmail.delete(0, Tk.END)
        self.enterpass.delete(0, Tk.END)
        self.enterpass2.delete(0, Tk.END)

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)

    def validate_email(self,userName,email):  #validates the email address by sending a verification code

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
            return randNo
        except smtplib.SMTPException:
            return 1




########################################################################################################################
#                                       CLASS INTERFACE FOR USER WINDOW                                               #
########################################################################################################################

class UserWin(Tk.Frame):

    def __init__(self, master):

        ##########################
        # SETTING UP THE WIDGETS #
        ##########################

        Tk.Frame.__init__(self, master, bg="#21618c")

        self.master.title("USER HOME")

        self.wLabel = Tk.Label(self, text="WELCOME, {0}!".format(user.name),
                               anchor=Tk.CENTER,
                               font=('Britannic Bold', 35),
                               fg="#f4d03f", bg="#21618c"
                               )

        self.pwdLabel = Tk.Label(self, text="Password:\n{0}".format(user.pwd),
                                 anchor=Tk.W,
                                 justify=Tk.LEFT,
                                 font=('Trebuchet', 18, "bold"),
                                 fg="#f4d03f", bg="#21618c",
                                 )

        self.emailLabel = Tk.Label(self, text="Correspondence Email:\n{0}".format(user.email),
                                   anchor=Tk.W,
                                   justify=Tk.LEFT,
                                   font=('Trebuchet', 18, "bold"),
                                   fg="#f4d03f", bg="#21618c"
                                   )

        self.monthLabel = Tk.Label(self, text="Monthly Expenses:\n{0}".format(self.month_expenses()),
                                   anchor=Tk.W,
                                   justify=Tk.LEFT,
                                   font=('Trebuchet', 18, "bold"),
                                   fg="#f4d03f", bg="#21618c"
                                   )

        self.yearLabel = Tk.Label(self, text="Yearly Expenses:\n{0}".format(self.year_expenses()),
                                  anchor=Tk.W,
                                  justify=Tk.LEFT,
                                  font=('Trebuchet', 18, "bold"),
                                  fg="#f4d03f", bg="#21618c"
                                  )

        self.budgetLabel = Tk.Label(self, text="Monthly Budget:\n{0}".format(user.budget),
                                    anchor=Tk.W,
                                    justify=Tk.LEFT,
                                    font=('Trebuchet', 18, "bold"),
                                    fg="#f4d03f", bg="#21618c"
                                    )

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(10):
            self.rowconfigure(row, weight=1)
        for col in range(6):
            self.columnconfigure(col, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        self.wLabel.grid(row=1, column=1, columnspan=4, sticky="news")
        self.pwdLabel.grid(row=3, column=2, sticky="news")
        self.emailLabel.grid(row=5, column=2, sticky="news")
        self.monthLabel.grid(row=3, column=4, sticky="news")
        self.yearLabel.grid(row=5, column=4, sticky="news")
        self.budgetLabel.grid(row=7, column=4, sticky="news")

    ####################
    #  CLASS METHODS   #
    ####################

    @staticmethod
    def month_expenses():

        today = localtime()

        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("SELECT SUM(price) FROM purchases WHERE month=? AND year=? AND userID=?",
                        (today[1], today[0], user.user_id))
            res = cur.fetchone()

        if res[0] is None:
            return 0.00
        else:
            return res[0]

    @staticmethod
    def year_expenses():

        today = localtime()

        with sqlite3.connect(database) as db:
            cur = db.cursor()
            cur.execute("SELECT SUM(price) FROM purchases WHERE year=? AND userID=?",
                        (today[0], user.user_id))
            res = cur.fetchone()

        if res[0] is None:
            return 0.00
        else:
            return res[0]

    def reset(self):
        self.master.config(menu=menuBar)
        self.wLabel.configure(text="WELCOME, {0}!".format(user.name))
        self.pwdLabel.configure(text="Password\n{0}".format(user.pwd))
        self.emailLabel.configure(text="Correspondence Email\n{0}".format(user.email))
        self.monthLabel.configure(text="Monthly Expenses\n{0}".format(self.month_expenses()))
        self.yearLabel.configure(text="Yearly Expenses\n{0}".format(self.year_expenses()))
        self.budgetLabel.configure(text="Monthly Budget\n{0}".format(user.budget))
        statBar.configure(bg="black", relief=Tk.SUNKEN, text="Currently signed in as {0}".format(user.name))

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)

    def leave(self):
        file_obj = open("remember_me.txt", "w")
        file_obj.write("")
        file_obj.close()
        self.master.config(menu="")
        startWin.tkraise()

########################################################################################################################
#                                       CLASS INTERFACE FOR USER WINDOW                                                #
########################################################################################################################

class ExpenseWin(Tk.Frame):

    def __init__(self, master):

        Tk.Frame.__init__(self, master)

        #################################
        # WIDGETS FOR THE EXPENSE TABLE #
        #################################

        self.canvas = Tk.Canvas(self, bg="#21618c")
        self.inFrame = Tk.Frame(self.canvas, bg="#21618c")
        self.vsb = Tk.Scrollbar(self, orient=Tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        #######################
        # REST OF THE WIDGETS #
        #######################

        self.filterBn = Tk.Button(self,
                                  text="Filter Results",
                                  font=('Calibri', 18),
                                  fg="#f4d03f", bg="#424949",
                                  activebackground="#797d7f",
                                  command=self.filter_results)

        self.addBn = Tk.Button(self,
                               text="Add Expense",
                               font=('Calibri', 18),
                               fg="#f4d03f", bg="#424949",
                               activebackground="#797d7f",
                               command=lambda: addWin.tkraise())

        self.delBn = Tk.Button(self,
                               text="Delete Expense",
                               font=('Calibri', 18),
                               fg="#f4d03f", bg="#424949",
                               activebackground="#797d7f",
                               command=self.delete)

        self.editBn = Tk.Button(self,
                                text="Edit Expense",
                                font=('Calibri', 18),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f",
                                command=editWin.tkraise)

        self.descEntry = Tk.Entry(self,
                                  font=('Calibri', 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)

        self.locEntry = Tk.Entry(self,
                                 font=('Calibri', 18),
                                 fg="#000000",
                                 justify=Tk.LEFT,
                                 relief=Tk.SUNKEN,
                                 bd=3)
        self.locBn = Tk.Menubutton(self,
                                   text="V",
                                   font=('Calibri', 18, "bold"),
                                   relief=Tk.RAISED)
        self.locMenu = Tk.Menu(self.locBn, tearoff=0)
        for loc in user.locs:
            self.locMenu.add_command(label=loc,
                                     command=lambda: self.locEntry.configure(text=loc))

        self.catEntry = Tk.Entry(self,
                                 font=('Calibri', 18),
                                 fg="#000000",
                                 justify=Tk.LEFT,
                                 relief=Tk.SUNKEN,
                                 bd=3)
        self.catBn = Tk.Menubutton(self,
                                   text="V",
                                   font=('Calibri', 18, "bold"),
                                   relief=Tk.RAISED)
        self.catMenu = Tk.Menu(self.catBn, tearoff=0)
        for cat in user.cats:
            self.catMenu.add_command(label=cat,
                                     command=lambda: self.catEntry.configure(text=cat))

        self.priceEntry = Tk.Entry(self,
                                   font=('Calibri', 18),
                                   fg="#000000",
                                   justify=Tk.LEFT,
                                   relief=Tk.SUNKEN,
                                   bd=3)

        self.dayEntry = Tk.Entry(self,
                                 font=('Calibri', 18),
                                 fg="#000000",
                                 justify=Tk.LEFT,
                                 relief=Tk.SUNKEN,
                                 bd=3)

        self.monthBn = Tk.Menubutton(self,
                                     text="Month",
                                     font=('Calibri', 18),
                                     relief=Tk.RAISED)

        self.monthMenu = Tk.Menu(self.monthBn, tearoff=0)
        for i in range(12):
            self.monthMenu.add_command(label="{0} - {1}".format(i+1, months[i]),
                                       command=lambda: self.monthBn.configure(text="{0} - {1}".format(i+1, months[i])))

        self.yearEntry = Tk.Entry(self,
                                  font=('Calibri', 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)









root = Tk.Tk()
root.state('zoomed')
#root.iconbitmap(default=r"C:\Users\James\Downloads\1497972677_Money.ico")  # CHANGE THIS ON YOUR LAPTOP
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
statBar = Tk.Label(root,
                   text="Currently not signed in!",
                   anchor=Tk.W,
                   relief=Tk.SUNKEN,
                   font=('Courier', 16),
                   bg="black", fg="white")
statBar.grid(row=1, column=0, sticky="news")


signupWin = SignupWin(root)
loginWin = LoginWin(root)
startWin = StartWin(root)
userWin = UserWin(root)
for frame in (loginWin, startWin, signupWin, userWin):
    frame.grid(row=0, column=0, sticky='news')
menuBar = Tk.Menu(root, tearoff=0)
menuBar.add_command(label="Expenses", command=loginWin.tkraise) # FOR NOW IT'S LOGINWIN
menuBar.add_command(label="Account", command=loginWin.tkraise)
menuBar.add_command(label="Email Report", command=userWin.tkraise)
menuBar.add_command(label="Logout", command=userWin.leave)

try:
    file_obj = open("remember_me.txt", "r")
    with sqlite3.connect(database) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE userID=?",(int(file_obj.read()),))
        res = cur.fetchone()
    user.user_id = res[0]
    user.name = res[1]
    user.pwd = res[2]
    user.budget = res[3]
    user.email = res[4]
    userWin.tkraise()
except:
    startWin.tkraise()

root.mainloop()
