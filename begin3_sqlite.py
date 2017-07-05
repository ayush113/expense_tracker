import Tkinter as Tk
import sqlite3
import smtplib
from email import Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from time import localtime, sleep
from datetime import date
from random import randint

db_name = "Accounts.db"

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
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO users(userName, pwd, budget, email) VALUES (?,?,?,?)",
                        (self.name, self.pwd, self.budget, self.email))
            db.commit()

    def edit(self):  # EDITS USER'S DETAILS AND UPDATES THEM IN DATABASE
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("UPDATE users SET userName=?, pwd=?, budget=?, email=? WHERE userID=?",
                        (self.name, self.pwd, self.budget, self.email, self.user_id))
            db.commit()

    def delete(self):  # DELETES USER ACCOUNT FROM DATABASE
        with sqlite3.connect(db_name) as db:
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
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO purchases(userID, dscr, cat, loc, day, month, year, price) "
                        "VALUES (?,?,?,?,?,?,?,?)",
                        (self.user_id, self.dscr, self.cat, self.loc,
                         self.day, self.month, self.year,
                         self.price))
            db.commit()

    def edit_expense(self):  # EDITS EXPENSE WITH PURCHASE (DICTIONARY) AND UPDATES TO DATABASE
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("UPDATE purchases SET userID=?, dscr=?, cat=?, loc=?, day=?, month=?, year=?, price=? "
                        "WHERE purchaseID=?",
                        (self.user_id, self.dscr, self.cat, self.loc,
                         self.day, self.month, self.year,
                         self.price, self.purchase_id))
            db.commit()

    def delete_expense(self):  # DELETES EXPENSE FROM DATABASE
        with sqlite3.connect(db_name) as db:
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

    with sqlite3.connect(db_name) as db:
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

        with sqlite3.connect(db_name) as db:
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

        with sqlite3.connect(db_name) as db:
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

        # TITLE
        self.label = Tk.Label(self, text="CREATE A NEW ACCOUNT!",
                              anchor=Tk.CENTER,
                              font=("Britannic Bold", 35),
                              fg="#f4d03f", bg="#21618c")

        # USER PACKAGE
        self.userLabel = Tk.Label(self, text="Enter a Username (minimum 5 characters)",
                                  anchor=Tk.W,
                                  font=("Calibri", 18),
                                  fg="#f4d03f",bg="#21618c")

        self.userEntry = Tk.Entry(self, font=("Calibri", 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)

        # PASSWORD PACKAGE
        self.pwdLabel = Tk.Label(self, text="Enter a Password (minimum 6 characters)",
                                 anchor=Tk.W,
                                 font=("Calibri", 18),
                                 fg="#f4d03f", bg="#21618c")

        self.pwdEntry = Tk.Entry(self, show="*",
                                 font=("Calibri", 18),
                                 fg="#000000", justify=Tk.LEFT,
                                 relief=Tk.SUNKEN,
                                 bd=3)

        self.pwdCLabel = Tk.Label(self, text="Confirm the Password",
                                  anchor=Tk.W,
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#21618c")

        self.pwdCEntry = Tk.Entry(self, show="*",
                                  font=("Calibri", 18),
                                  fg="#000000", justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)

        self.showLabel = Tk.Label(self, text="Show",
                                  anchor=Tk.CENTER,
                                  font=("Calibri", 18),
                                  fg="#f4d03f",
                                  bg="#424949",
                                  relief=Tk.FLAT)

        # EMAIL PACKAGE
        self.emailLabel = Tk.Label(self, text="Enter a Valid Email Address",
                                   anchor=Tk.W,
                                   font=("Calibri", 18),
                                   fg="#f4d03f", bg="#21618c")

        self.emailEntry = Tk.Entry(self, font=("Calibri", 18),
                                   fg="#000000",
                                   justify=Tk.LEFT,
                                   relief=Tk.SUNKEN,
                                   bd=3)

        # BUDGET PACKAGE
        self.budgLabel = Tk.Label(self, text="Enter a Monthly Budget for Your Expenses",
                                  anchor=Tk.W,
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#21618c")

        self.budgEntry = Tk.Entry(self, font=("Calibri", 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  bd=3)

        # STANDARD BUTTONS
        self.backBn = Tk.Button(self, text="Back",
                                font=("Calibri", 18),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f",
                                command=lambda: startWin.tkraise())

        self.signupBn = Tk.Button(self, text="Sign Up!",
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#424949",
                                  activebackground="#797d7f",
                                  command=self.signup)
        self.users = []
        self.emails = []

        self.showLabel.bind("<Motion>", self.show_pwd)
        self.showLabel.bind("<Leave>", self.hide_pwd)

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(21):
            self.rowconfigure(row, weight=1)
        for col in range(10):
            self.columnconfigure(col, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        # TITLE
        self.label.grid(row=1, column=3, columnspan=4, sticky="news")

        # USERNAME PACKAGE
        self.userLabel.grid(row=4, column=3, sticky="news")
        self.userEntry.grid(row=4, column=5, columnspan=2, sticky="news")

        # PASSWORD PACKAGE
        self.pwdLabel.grid(row=8, column=3, sticky="news")
        self.pwdCLabel.grid(row=10, column=3, sticky="news")
        self.pwdEntry.grid(row=8, column=5, sticky="news")
        self.pwdCEntry.grid(row=10, column=5, columnspan=2, sticky="news")
        self.showLabel.grid(row=8, column=6, sticky="news")

        # EMAIL PACKAGE
        self.emailLabel.grid(row=6, column=3, sticky="news")
        self.emailEntry.grid(row=6, column=5, columnspan=2, sticky="news")

        # BUDGET PACKAGE
        self.budgLabel.grid(row=12, column=3, sticky="news")
        self.budgEntry.grid(row=12, column=5, columnspan=2, sticky="news")

        # STANDARD BUTTONS
        self.backBn.grid(row=19, column=7, sticky="news")
        self.signupBn.grid(row=15, column=4, sticky="news")

    #################
    # CLASS METHODS #
    #################

    def show_pwd(self, event=None):
        self.pwdEntry.configure(show="")
        self.pwdCEntry.configure(show="")

    def hide_pwd(self, event=None):
        self.pwdEntry.configure(show="*")
        self.pwdCEntry.configure(show="*")

    def signup(self):

        user_name = self.userEntry.get()
        pwd = self.pwdEntry.get()
        pwd_c = self.pwdCEntry.get()
        email = self.emailEntry.get()
        budget = self.budgEntry.get()

        err_msg = "ERROR/INVALID: "

        if len(user_name)<5:
            err_msg += "USERNAME, "
        if len(pwd)<6:
            err_msg += "PASSWORD, "
        if len(email) <= 0:
            err_msg += "EMAIL, "
        if not budget.isdigit():
            err_msg += "BUDGET, "
        else:
            if float(budget) <= 0.0:
                err_msg += "BUDGET, "
        if pwd != pwd_c:
            err_msg = err_msg[:-2] + "; PASSWORDS DON'T MATCH; "
        if user_name in self.users:
            err_msg += "USERNAME ALREADY EXISTS; "
        if email in self.emails:
            err_msg += "EMAIL ID ALREADY IN USE! "
        err_msg = err_msg[:-2]+"!"

        if len(err_msg) == 14:
            code_num = randint(10000, 99999)
            subject = "Account Verification"
            message = "<p>Dear %s,</p><p>\nBelow is the verification code for completion of registration on " \
                      "Expense Tracker 9000XL.</p><p>\nEnter the code in the program to complete registration.\n</p>" \
                      "<h1><b>%d</b></h1>" % (user_name, code_num)
            if send_mail(subject, message, [], user_name, email):
                statBar.configure(bg="black", relief=Tk.SUNKEN,
                                  text="VERIFICATION CODE SENT! CHECK INBOX @ {0}".format(email))
                user.name = user_name
                user.email = email
                user.pwd = pwd
                user.budget = budget
                verifyWin.tkraise(code_num)
            else:
                statBar.configure(bg="red", relief=Tk.RAISED,
                                  text="COULD NOT SEND VERIFICATION CODE! ENSURE INTERNET CONNECTION "
                                       "AND VALID EMAIL ADDRESS")
        else:
            statBar.configure(bg="red", relief=Tk.RAISED, text=err_msg)

    def reset(self):
        self.master.title("SIGN UP")
        statBar.configure(bg="black", text="Currently not signed in!", relief=Tk.SUNKEN)
        self.userEntry.delete(0, Tk.END)
        self.emailEntry.delete(0, Tk.END)
        self.pwdEntry.delete(0, Tk.END)
        self.pwdCEntry.delete(0, Tk.END)
        self.budgEntry.delete(0, Tk.END)
        self.users = []
        self.emails = []
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT userName FROM users")
            res = cur.fetchone()
            while res:
                self.users.append(res[0])
                res = cur.fetchone()
            cur.execute("SELECT email FROM users")
            res = cur.fetchone()
            while res:
                self.emails.append(res[0])
                res = cur.fetchone()

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)

########################################################################################################################
#                                       CLASS INTERFACE FOR VERIFICATION WINDOW                                        #
########################################################################################################################

class VerifyWin(Tk.Frame):

    code_num = 0

    def __init__(self, master):

        Tk.Frame.__init__(self, master, bg="#21618c")

        ##########################
        # SETTING UP THE WIDGETS #
        ##########################

        self.label = Tk.Label(self, text="ACCOUNT VERIFICATION",
                                  anchor=Tk.CENTER,
                                  font=("Britannic Bold", 35),
                                  fg="#f4d03f", bg="#21618c")

        self.codeLabel = Tk.Label(self, text="Enter the Verification Code      ",
                                  anchor=Tk.E,
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#21618c")

        self.codeEntry = Tk.Entry(self, font=("Calibri", 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  disabledbackground="#21618c",
                                  bd=3)

        self.verifyBn = Tk.Button(self, text="Verify",
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#424949",
                                  activebackground="#797d7f",
                                  command=self.verify)

        self.backBn = Tk.Button(self, text="Back",
                                font=("Calibri", 18),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f",
                                command=self.leave)

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(5):
            self.rowconfigure(row, weight=1)
        for col in range(6):
            self.columnconfigure(col, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        self.label.grid(row=0, column=1, columnspan=4, sticky="news")
        self.codeLabel.grid(row=1, column=1, sticky="news")
        self.codeEntry.grid(row=1, column=3, sticky="ew")
        self.verifyBn.grid(row=2, column=2, sticky="ew")
        self.backBn.grid(row=4, column=4, sticky="ew")

    #################
    # CLASS METHODS #
    #################

    def verify(self):

        if self.codeEntry.get() == str(self.code_num):
            user.create()
            userWin.tkraise()
        else:
            statBar.configure(bg="red", relief=Tk.RAISED,
                              text="INCORRECT VERIFICATION CODE!"
                                   "CLICK <BACK> TO RETURN TO SIGNUP MENU AND RE-SEND VERIFICATION EMAIL")
            user.clear()

    @staticmethod
    def leave():
        user.clear()
        signupWin.tkraise()

    def tkraise(self, code_num):
        self.code_num = code_num
        self.codeEntry.delete(0, Tk.END)
        Tk.Frame.tkraise(self)

########################################################################################################################
#                                       CLASS INTERFACE FOR USER WINDOW                                                #
########################################################################################################################

class UserWin(Tk.Frame):

    def __init__(self, master):

        ##########################
        # SETTING UP THE WIDGETS #
        ##########################

        Tk.Frame.__init__(self, master, bg="#21618c")

        self.master.title("USER DASHBOARD")

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

        with sqlite3.connect(db_name) as db:
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

        with sqlite3.connect(db_name) as db:
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
        self.master.title("USER DASHBOARD")
        self.wLabel.configure(text="WELCOME, {0}!".format(user.name))
        self.pwdLabel.configure(text="Password\n{0}".format(user.pwd))
        self.emailLabel.configure(text="Correspondence Email\n{0}".format(user.email))
        self.monthLabel.configure(text="Monthly Expenses\n{0}".format(self.month_expenses()))
        self.yearLabel.configure(text="Yearly Expenses\n{0}".format(self.year_expenses()))
        self.budgetLabel.configure(text="Monthly Budget\n{0}".format(float(user.budget)))
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
#                                       CLASS INTERFACE FOR ACCOUNT DETAILS WINDOW                                     #
########################################################################################################################

class AccountWin(Tk.Frame):

    def __init__(self, master):

        Tk.Frame.__init__(self, master, bg="#21618c")

        ##########################
        # SETTING UP THE WIDGETS #
        ##########################

        self.master.title("ACCOUNT DETAILS")

        # TITLE
        self.label = Tk.Label(self, text="EDIT ACCOUNT DETAILS!",
                              anchor=Tk.CENTER,
                              font=("Britannic Bold", 35),
                              fg="#f4d03f", bg="#21618c")

        # USER PACKAGE
        self.userLabel = Tk.Label(self, text="Enter a Username (minimum 5 characters)",
                                  anchor=Tk.W,
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#21618c")

        self.userEntryVar = Tk.StringVar(value='')

        self.userEntry = Tk.Entry(self, font=("Calibri", 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  textvariable=self.userEntryVar,
                                  bd=3)

        # PASSWORD PACKAGE
        self.pwdLabel = Tk.Label(self, text="Enter a Password (minimum 6 characters)",
                                 anchor=Tk.W,
                                 font=("Calibri", 18),
                                 fg="#f4d03f", bg="#21618c")

        self.pwdEntryVar = Tk.StringVar(value='')

        self.pwdEntry = Tk.Entry(self, show="*",
                                 font=("Calibri", 18),
                                 fg="#000000", justify=Tk.LEFT,
                                 relief=Tk.SUNKEN,
                                 textvariable=self.pwdEntryVar,
                                 bd=3)

        self.pwdCLabel = Tk.Label(self, text="Confirm the Password",
                                  anchor=Tk.W,
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#21618c")

        self.pwdCEntryVar = Tk.StringVar(value='')

        self.pwdCEntry = Tk.Entry(self, show="*",
                                  font=("Calibri", 18),
                                  fg="#000000", justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  textvariable=self.pwdCEntryVar,
                                  bd=3)

        self.showLabel = Tk.Label(self, text="Show",
                                  anchor=Tk.CENTER,
                                  font=("Calibri", 18),
                                  fg="#f4d03f",
                                  bg="#424949",
                                  relief=Tk.FLAT)

        # EMAIL PACKAGE
        self.emailLabel = Tk.Label(self, text="Email Address (cannot be changed)",
                                   anchor=Tk.W,
                                   font=("Calibri", 18),
                                   fg="#f4d03f", bg="#21618c")

        self.emailEntryVar = Tk.StringVar(value='')

        self.emailEntry = Tk.Entry(self, font=("Calibri", 18),
                                   fg="#000000",
                                   justify=Tk.LEFT,
                                   relief=Tk.SUNKEN,
                                   state=Tk.DISABLED,
                                   textvariable=self.emailEntryVar,
                                   bd=3)

        # BUDGET PACKAGE
        self.budgLabel = Tk.Label(self, text="Enter a Monthly Budget for Your Expenses",
                                  anchor=Tk.W,
                                  font=("Calibri", 18),
                                  fg="#f4d03f", bg="#21618c")

        self.budgEntryVar = Tk.StringVar(value='')

        self.budgEntry = Tk.Entry(self, font=("Calibri", 18),
                                  fg="#000000",
                                  justify=Tk.LEFT,
                                  relief=Tk.SUNKEN,
                                  textvariable=self.budgEntryVar,
                                  bd=3)

        # STANDARD BUTTONS
        self.saveBn = Tk.Button(self, text="Save Changes",
                                font=("Calibri", 18),
                                fg="#f4d03f", bg="#424949",
                                activebackground="#797d7f",
                                command=self.save)
        self.users = []

        self.showLabel.bind("<Motion>", self.show_pwd)
        self.showLabel.bind("<Leave>", self.hide_pwd)

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(21):
            self.rowconfigure(row, weight=1)
        for col in range(10):
            self.columnconfigure(col, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        # TITLE
        self.label.grid(row=1, column=3, columnspan=4, sticky="news")

        # USERNAME PACKAGE
        self.userLabel.grid(row=4, column=3, sticky="news")
        self.userEntry.grid(row=4, column=5, columnspan=2, sticky="news")

        # PASSWORD PACKAGE
        self.pwdLabel.grid(row=8, column=3, sticky="news")
        self.pwdCLabel.grid(row=10, column=3, sticky="news")
        self.pwdEntry.grid(row=8, column=5, sticky="news")
        self.pwdCEntry.grid(row=10, column=5, columnspan=2, sticky="news")
        self.showLabel.grid(row=8, column=6, sticky="news")

        # EMAIL PACKAGE
        self.emailLabel.grid(row=6, column=3, sticky="news")
        self.emailEntry.grid(row=6, column=5, columnspan=2, sticky="news")

        # BUDGET PACKAGE
        self.budgLabel.grid(row=12, column=3, sticky="news")
        self.budgEntry.grid(row=12, column=5, columnspan=2, sticky="news")

        # STANDARD BUTTONS
        self.saveBn.grid(row=15, column=4, sticky="news")

    #################
    # CLASS METHODS #
    #################

    def show_pwd(self, event=None):
        self.pwdEntry.configure(show="")
        self.pwdCEntry.configure(show="")

    def hide_pwd(self, event=None):
        self.pwdEntry.configure(show="*")
        self.pwdCEntry.configure(show="*")

    def save(self):

        user_name = self.userEntryVar.get()
        pwd = self.pwdEntryVar.get()
        pwd_c = self.pwdCEntryVar.get()
        budget = self.budgEntryVar.get()

        err_msg = "ERROR/INVALID: "

        if len(user_name) < 5:
            err_msg += "USERNAME, "
        if len(pwd) < 6:
            err_msg += "PASSWORD, "
        if not ("".join(budget.split("."))).isdigit():
            err_msg += "BUDGET, "
        else:
            if float(budget) <= 0.0:
                err_msg += "BUDGET, "
        if pwd != pwd_c:
            err_msg = err_msg[:-2] + ". PASSWORDS DON'T MATCH; "
        if user_name in self.users and user_name != user.name:
            err_msg += "USERNAME ALREADY EXISTS; "
        err_msg = err_msg[:-2]+"!"

        if len(err_msg) == 14:
            user.name = user_name
            user.pwd = pwd
            user.budget = budget
            user.edit()
            statBar.configure(bg="#27ae60", relief=Tk.SUNKEN, text="CHANGES IN ACCOUNT DETAILS SAVED SUCCESSFULLY!")
        else:
            statBar.configure(bg="red", relief=Tk.RAISED, text=err_msg)

    def reset(self):
        self.master.title("ACCOUNT DETAILS")
        statBar.configure(bg="black", text="Currently signed in as {0}".format(user.name), relief=Tk.SUNKEN)
        self.userEntryVar.set(user.name)
        self.pwdEntryVar.set(user.pwd)
        self.pwdCEntryVar.set(user.pwd)
        self.budgEntryVar.set(user.budget)
        self.emailEntryVar.set(user.email)
        self.users = []
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT userName FROM users")
            res = cur.fetchone()
            while res:
                self.users.append(res[0])
                res = cur.fetchone()

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)

########################################################################################################################
#                                   CLASS INTERFACE FOR EMAIL REPORTS WINDOW                                           #
########################################################################################################################

class ReportsWin(Tk.Frame):

    def __init__(self, master):

        Tk.Frame.__init__(self, master, bg="#21618c")


########################################################################################################################
#                                       CLASS INTERFACE FOR USER WINDOW                                                #
########################################################################################################################

class ExpenseWin(Tk.Frame):

    def __init__(self, master):

        Tk.Frame.__init__(self, master, bg="#21618c")

        #################################
        # WIDGETS FOR THE EXPENSE TABLE #
        #################################

        self.canvas = Tk.Canvas(self, bg="#21618c")
        self.frame = Tk.Frame(self.canvas, bg="#21618c")
        self.vsb = Tk.Scrollbar(self, orient=Tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.create_window((0, 0), window=self.frame, anchor=Tk.NW)
        self.bind("<Configure>", lambda x: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.master.bind_class("Label", "<Button-1>", self.choose)
        self.master.bind_class("Label", "<Enter>", self.highlight)
        self.master.bind_class("Label", "<Leave>", self.highlight)
        self.res = []  # HOLDS ALL THE RESULTS OF A PARTICULAR SEARCH OR ALL EXPENSES
        self.titles = ("Description", "Category", "Location", "Amount", "Day", "Month", "Year")
        self.highlight_clr = "#21618c"
        self.cur_row = None

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
                               command=self.add)

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
                                command=self.edit)

        self.clearBn = Tk.Button(self,
                                 text="Clear Entries",
                                 font=('Calibri', 18),
                                 fg="#f4d03f", bg="#424949",
                                 activebackground="#797d7f",
                                 command=self.reset)

        '''self.idLabel = Tk.Message(self,
                                  anchor=Tk.W,
                                  font=('Trebuchet', 18),
                                  fg="#f4d03f",
                                  bg="#21618c"
                                  )'''

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

        ##########################
        # SETTING UP THE LAYOUT  #
        ##########################

        for row in range(7):
            self.rowconfigure(row, weight=1)
        for col in range(9):
            self.columnconfigure(col, weight=1)

        self.frame.rowconfigure(0, weight=1)
        for i in range(7):
            self.frame.columnconfigure(i, weight=1)

        #########################
        # DISPLAYING ON WINDOW  #
        #########################

        self.addBn.grid(row=1, column=2, sticky="news")
        self.delBn.grid(row=1, column=3, sticky="news")
        self.editBn.grid(row=1, column=4, sticky="news")
        self.filterBn.grid(row=1, column=5, sticky="news")
        self.clearBn.grid(row=1, column=6, sticky="news")
        self.descEntry.grid(row=3, column=1, sticky="news")
        self.catEntry.grid(row=3, column=2, sticky="news")
        self.catBn.grid(row=3, column=2, sticky="ns")
        self.locEntry.grid(row=3, column=3, sticky="news")
        self.locBn.grid(row=3, column=3, sticky="ns")
        self.priceEntry.grid(row=3, column=4, sticky="news")
        self.dayEntry.grid(row=3, column=5, sticky="news")
        # self.monthMenu.pack(side="left", fill="both", expand=True)
        self.monthBn.grid(row=3, column=6, sticky="news")
        self.yearEntry.grid(row=3, column=7, sticky="news")

        self.canvas.grid(row=6, column=1, columnspan=7, sticky="news")
        self.vsb.grid(row=6, column=8, sticky="ns")
        # THIS WAS THE MAIN REASON WHY THE CODE WASN'T WORKING.
        # ABOVE LINE IS A PIECE OF CRAP FOR SURE!
        # REPLACE THIS LINE WITH self.vsb.pack() TO HURT YOURSELF

    #################
    # CLASS METHODS #
    #################

    def reset(self):

        self.descEntry.delete(0, Tk.END)
        self.locEntry.delete(0, Tk.END)
        self.catEntry.delete(0, Tk.END)
        self.dayEntry.delete(0, Tk.END)
        self.yearEntry.delete(0, Tk.END)
        self.cur_row = None
        statBar.configure(bg="black", relief=Tk.SUNKEN, text="Currently signed in as {0}".format(user.name))
        # self.delBn.configure(state=Tk.DISABLED)
        # self.editBn.configure(state=Tk.DISABLED)
        # self.idLabel.configure(text="")
        self.monthBn.configure(text="Month")

        #self.locMenu.delete(0, Tk.END)  # ,len(user.locs)-1)
        for loc in user.locs:
            self.locMenu.add_command(label=loc,
                                     command=lambda: self.locEntry.configure(text=loc))

        #self.catMenu.delete(0, Tk.END)  # ,len(user.cats)-1)
        for cat in user.cats:
            self.catMenu.add_command(label=cat,
                                     command=lambda: self.catEntry.configure(text=cat))

        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT purchaseID, dscr, cat, loc, price, day, month, year FROM purchases WHERE userID=?",
                        (user.user_id,))
            self.res = cur.fetchall()

        self.display()

    def highlight(self, event):
        row = event.widget.grid_info()["row"]
        if self.highlight_clr == "#21618c":
            self.highlight_clr = "#000000"
        else:
            self.highlight_clr = "#21618c"
        for label in self.frame.grid_slaves(row=row):
            label.configure(bg=self.highlight_clr)

    def choose(self, event):
        # self.delBn.configure(state=Tk.NORMAL)
        # self.editBn.configure(state=Tk.NORMAL)
        self.cur_row = event.widget.grid_info()["row"]
        label_list = self.frame.grid_slaves(row=self.cur_row)
        self.descEntry.configure(text=label_list[6])
        self.catEntry.configure(text=label_list[5])
        self.locEntry.configure(text=label_list[4])
        self.priceEntry.configure(text=label_list[3])
        self.dayEntry.configure(text=label_list[2])
        self.monthBn.configure(text="{0} - {1}".format(label_list[1], months[label_list[1]-1]))
        self.yearEntry.configure(text=label_list[0])
        # self.idLabel.configure(text=label_list[0])

    def delete(self):

        if self.cur_row:
            purchase.purchase_id = self.res[self.cur_row-1][0]
            purchase.delete_expense()
            statBar.configure(bg="black", relief=Tk.SUNKEN, text="SUCCESSFULLY DELETED!")
        else:
            statBar.configure(bg="red", relief=Tk.RAISED, text="COULD NOT DELETE EXPENSE!")

    def check_expense(self):

        err_msg = "INVALID"
        if not self.descEntry.get():
            err_msg += "DESCRIPTION, "
        if not self.catEntry.get():
            err_msg += "CATEGORY, "
        if not self.locEntry.get():
            err_msg += "LOCATION, "
        if not ("".join(self.priceEntry.get().split("."))).isdigit():
            # FIRST, SPLIT AT DECIMAL POINT AND THEN JOIN WHAT'S LEFT AND IF THOSE ARE DIGITS, IT'LL BE VALID
            err_msg += "AMOUNT, "
        try:
            date(int(self.yearEntry.get()), self.monthBn.cget("text")[0:2], int(self.dayEntry.get()))
        except ValueError:
            err_msg += "DATE, "
        return err_msg

    def edit(self):

        if self.cur_row:
            err_msg = self.check_expense()
            if len(err_msg) != 7:
                purchase.user_id = user.user_id
                purchase.purchase_id = self.res[self.cur_row - 1][0]
                purchase.dscr = self.descEntry.get()
                purchase.cat = self.catEntry.get()
                purchase.loc = self.locEntry.get()
                purchase.day = int(self.dayEntry.get())
                purchase.month = int(self.monthBn.cget("text")[0:2])
                purchase.year = int(self.yearEntry.get())
                purchase.price = float(self.priceEntry.get())
                purchase.edit_expense()
                statBar.configure(bg="black", relief=Tk.SUNKEN, text="SUCCESSFULLY EDITED!")
            else:
                statBar.configure(bg="red", relief=Tk.RAISED, text=err_msg + "PLEASE RE-CHECK DETAILS!")
        else:
            statBar.configure(bg="red", relief=Tk.RAISED, text="COULD NOT EDIT EXPENSE!")

    def add(self):

        err_msg = self.check_expense()
        if len(err_msg) != 7:
            purchase.user_id = user.user_id
            purchase.purchase_id = self.res[self.cur_row - 1][0]
            purchase.dscr = self.descEntry.get()
            purchase.cat = self.catEntry.get()
            purchase.loc = self.locEntry.get()
            purchase.day = int(self.dayEntry.get())
            purchase.month = int(self.monthBn.cget("text")[0:2])
            purchase.year = int(self.yearEntry.get())
            purchase.price = float(self.priceEntry.get())
            purchase.add_expense()
            statBar.configure(bg="black", relief=Tk.SUNKEN, text="SUCCESSFULLY ADDED!")
        else:
            statBar.configure(bg="red", relief=Tk.RAISED, text=err_msg + "PLEASE RE-CHECK DETAILS!")

    def filter_results(self):

        self.cur_row = None
        query = "SELECT dscr, cat, loc, price, day, month, year FROM purchases WHERE userID=?"

        if self.descEntry.get():
            query += " AND dscr LIKE '%{0}%'".format(self.descEntry.get())
        if self.catEntry.get():
            query += " AND cat='{0}'".format(self.catEntry.get())
        if self.locEntry.get():
            query += " AND loc='{0}'".format(self.locEntry.get())
        if self.priceEntry.get():
            query += " AND price={0}".format(self.priceEntry.get())
        if self.dayEntry.get():
            query += " AND day={0}".format(self.dayEntry.get())
        if self.monthBn.cget("text") != "Month":
            query += " AND month={0}".format(self.monthBn.cget("text")[0:2])
        if self.yearEntry.get():
            query += " AND year={0}".format(self.yearEntry.get())

        try:
            with sqlite3.connect(db_name) as db:
                cur = db.cursor()
                cur.execute(query)
                self.res = cur.fetchall()
        except sqlite3.OperationalError:
            self.res = (("", "", "", "", "", "", ""),)

        self.display()

    def display(self):

        for i in range(7):
            Tk.Label(self.frame, text=self.titles[i], anchor=Tk.W, font=('Trebuchet', 14, "bold"), fg="#f4d03f",
                     bg="#21618c").grid(row=0, column=i, sticky="news")

        for row in range(len(self.res)):
            for col in range(7):
                Tk.Label(self.frame, text=str(self.res[row][col+1]), anchor=Tk.W, justify=Tk.LEFT, font=('Trebuchet', 14),
                         fg="#f4d03f", bg="#21618c").grid(row=row+1, column=col, sticky="news")
            self.frame.rowconfigure(row+1, weight=1)

    def tkraise(self):

        self.reset()
        Tk.Frame.tkraise(self)


# ensures referential integrity (https://pythonschool.net/databases/referential-integrity/)
with sqlite3.connect(db_name) as db:
    cur = db.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    db.commit()

try:  # checks if tables exist; if not, creates them
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        pick = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM purchases")
        pick = cur.fetchall()
        db.commit()

except sqlite3.OperationalError:
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS purchases")
        cur.execute("""CREATE TABLE users(userID INTEGER,
                                          userName TEXT,
                                          pwd TEXT,
                                          budget REAL,
                                          email TEXT,
                                          PRIMARY KEY(userID))""")

        cur.execute("""CREATE TABLE purchases(purchaseID INTEGER,
                                              dscr TEXT,
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
        db.commit()

# X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

root = Tk.Tk()
root.state('zoomed')
root.iconbitmap(default=r"C:\Users\James\Downloads\1497972677_Money.ico")  # CHANGE THIS ON YOUR LAPTOP
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
expenseWin = ExpenseWin(root)
verifyWin = VerifyWin(root)
accountWin = AccountWin(root)

for frame in (loginWin, startWin, signupWin, userWin, expenseWin, verifyWin, accountWin):
    frame.grid(row=0, column=0, sticky='news')

menuBar = Tk.Menu(root, tearoff=0)
menuBar.add_command(label="Dashboard", command=userWin.tkraise)
menuBar.add_command(label="Expenses", command=expenseWin.tkraise)
menuBar.add_command(label="Account", command=accountWin.tkraise)
menuBar.add_command(label="Email Report", command=loginWin.tkraise)  # FOR NOW IT'S LOGINWIN
menuBar.add_command(label="Logout", command=userWin.leave)
try:
    file_obj = open("remember_me.txt", "r")
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE userID=?", (int(file_obj.read()),))
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
