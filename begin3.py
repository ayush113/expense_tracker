import Tkinter as Tk
import pyodbc
import smtplib
from email import Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

server = "tcp:expense-tracker.database.windows.net"
database = "Accounts"
username = "aandj"
password = "extr@ck9000Xl"
driver = "{ODBC Driver 13 for SQL Server}"
cnxn = "DRIVER=" + driver + ";PORT=1433;SERVER=" + server + ";PORT=1443;DATABASE=" + database + \
       ";UID="+username+";PWD="+password

sendEmail = "expense.trackerxl@gmail.com"
sendPwd = "extrack9000"


########################################################################################################################
#                                       CLASS FOR USERS                                                                #
########################################################################################################################


class User(object):
    def __init__(self, user_id=0, name="", pwd="", budget=0.0, email=""):
        self.user_id = user_id
        self.name = name
        self.pwd = pwd
        self.budget = budget
        self.email = email

    def create(self):  # STORES USER'S DETAILS INTO DATABASE
        with pyodbc.connect(cnxn) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO users(name, pwd, budget, email) VALUES (?,?,?,?,?,?)",
                        (self.name, self.pwd, self.budget, self.email))
            db.commit()

    def edit(self):  # EDITS USER'S DETAILS AND UPDATES THEM IN DATABASE
        with pyodbc.connect(cnxn) as db:
            cur = db.cursor()
            cur.execute("UPDATE users SET userName=?, pwd=?, budget=?, email=? WHERE userID=?",
                        (self.name, self.pwd, self.budget, self.email, self.user_id))
            db.commit()

    def delete(self):  # DELETES USER ACCOUNT FROM DATABASE
        with pyodbc.connect(cnxn) as db:
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
        with pyodbc.connect(cnxn) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO purchases(userID, dscr, cat, loc, day, month, year, price) "
                        "VALUES (?,?,?,?,?,?,?,?)",
                        (self.user_id, self.dscr, self.cat, self.loc,
                         self.day, self.month, self.year,
                         self.price))
            db.commit()

    def edit_expense(self, purchase):  # EDITS EXPENSE WITH PURCHASE (DICTIONARY) AND UPDATES TO DATABASE
        with pyodbc.connect(cnxn) as db:
            cur = db.cursor()
            cur.execute("UPDATE purchases SET userID=?, dscr=?, cat=?, loc=?, day=?, month=?, year=?, price=? "
                        "WHERE purchaseID=?",
                        (self.user_id, self.dscr, self.cat, self.loc,
                         self.day, self.month, self.year,
                         self.price, self.purchase_id))
            db.commit()

    def delete_expense(self):  # DELETES EXPENSE FROM DATABASE
        with pyodbc.connect(cnxn) as db:
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

        with pyodbc.connect(cnxn) as db:
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

            if self.remVar == 1:
                file_obj = open("remember_me.txt", "w")
                file_obj.write(user.user_id)
                file_obj.close()

            userWin.reset()
            userWin.tkraise()

    def submit(self):

        with pyodbc.connect(cnxn) as db:
            cur = db.cursor()
            cur.execute("SELECT userName, pwd FROM users WHERE email=?", (forgotEntry.get(),))
            res = cur.fetchone()

        if res is None:
            statBar.bell()
            statBar.configure(bg="red", relief=Tk.RAISED, text="ERROR: EMAIL NOT FOUND!")
        else:
            message = "<p>Dear %s</p><p>You have requested your password to be sent to your email. " \
                      "Below is your password; please store it carefully for future reference</p>" \
                      "<h1><b>%s</b></h1>" % (res[0], res[1])
            subject = "Forgot Password"
            statBar.configure(bg="green", relief=Tk.SUNKEN, text="SENDING MAIL...")
            if send_mail(subject, message, [], res[0], forgotEntry.get()):
                statBar.configure(bg="black", relief=Tk.SUNKEN, text="MAIL SUCCESSFULLY SENT!")
            else:
                statBar.bell()
                statBar.configure(bg="red", relief=Tk.RAISED, text="ERROR: INTERNET CONNECTION NOT ESTABLISHED!")

########################################################################################################################
#                                       CLASS INTERFACE FOR SIGNUP WINDOW                                               #
########################################################################################################################

class SignupWin(Tk.Frame):

    def __init__(self,master):

        Tk.Frame.__init__(self, master, bg="#21618c")

                   ####  COPIED         ###
                   #### THE WIDGETS    ###

        self.master.title("SIGNUP !")

        self.label = Tk.Label(self,text = "CREATE A NEW ACCOUNT !",anchor=Tk.CENTER,
        font=("Britannic Bold", 35),fg="#f4d03f",bg="#21618c")

        self.unameLabel = Tk.Label(self,text = "Enter a Username",anchor=Tk.CENTER,
        font=("Calibri", 18),fg="#f4d03f",bg="#21618c")

        self.plabel = Tk.Label(self,text = "Enter a Password",anchor=Tk.CENTER,
        font=("Calibri", 18),fg="#f4d03f",bg="#21618c")

        self.plabelConf = Tk.Label(self,text = "Confirm the Password",anchor=Tk.CENTER,
        font=("Calibri", 18),fg="#f4d03f",bg="#21618c")

        self.email_label = Tk.Label(self,text = "Enter a Valid EmailID",anchor=Tk.CENTER,
        font=("Calibri", 18),fg="#f4d03f",bg="#21618c")

        self.enterUname = Tk.Entry(self,font=("Caliri", 18),
        fg="#000000",justify=Tk.LEFT,relief=Tk.SUNKEN,bd=3)

        self.enterpass = Tk.Entry(self,show="*",font=("Caliri", 18),
        fg="#000000",justify=Tk.LEFT,relief=Tk.SUNKEN,bd=3)

        self.enterpass2 = Tk.Entry(self,show="*",font=("Caliri", 18),
        fg="#000000",justify=Tk.LEFT,relief=Tk.SUNKEN,bd=3)

        self.enterEmail = Tk.Entry(self,font=("Caliri", 18),
        fg="#000000",justify=Tk.LEFT,relief=Tk.SUNKEN,bd=3)

        self.signupBn = Tk.Button(self,text="SUBMIT",font = ("Calibri", 18),
        fg = "#f4d03f",bg = "#424949",activebackground="#797d7f",command=self.submit)

        self.backBn = Tk.Button(self,text="Go Back",font=("Calibri", 18),fg="#f4d03f",
        bg="#424949",activebackground="#797d7f",command=lambda: startWin.tkraise())

        self.showLabel = Tk.Label(self, text="Show",anchor=Tk.CENTER,font=("Calibri",18),
        fg="#f4d03f", bg="#424949",relief=Tk.FLAT)

        self.showLabel.bind("<Motion>", lambda x: self.enterpass.configure(show=""))
        self.showLabel.bind("<Leave>", lambda x: self.enterpass.configure(show="*"))

        #####                            #####
        #####   Setting the layout grids #####

        for row in range(40):
            self.rowconfigure(row,weight=1)
        for col in range(20):
            self.columnconfigure(col,weight=1)

        #####      Thank Joshua !        #####
        #####  Putting it on the Display #####

        self.label.grid(row=3,column=6,rowspan=2,columnspan=9,sticky="news")
        self.unameLabel.grid(row=8,column=6,rowspan=2,columnspan=4,sticky="news")
        self.enterUname.grid(row=8,column=11,rowspan=2,columnspan=3,sticky="news")
        self.email_label.grid(row=12,column=6,rowspan=2,columnspan=4,sticky="news")
        self.enterEmail.grid(row=12,column=11,rowspan=2,columnspan=3,sticky="news")
        self.plabel.grid(row=16,column=6,rowspan=2,columnspan=4,sticky="news")
        self.enterpass.grid(row=16,column=11,rowspan=2,columnspan=3,sticky="news")
        self.plabelConf.grid(row=20,column=6,rowspan=2,columnspan=4,sticky="news")
        self.enterpass2.grid(row=20,column=11,rowspan=2,columnspan=3,sticky="news")
        self.signupBn.grid(row=26,column=7,rowspan=2,columnspan=3,sticky="news")
        self.backBn.grid(row=26,column=11,rowspan=2,columnspan=3,sticky="news")
        self.showLabel.grid(row=16,column=14,rowspan=2,columnspan=1,sticky="news")

        ####  COPYING JOSH IS FUN ####
        ####     CLASS METHODS    ####

    def submit(self):
        statBar.configure(bg="black",relief=Tk.SUNKEN,text="New User Details")
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
            with pyodbc.connect(cnxn) as db:
                cur = db.cursor()
                cur.execute("SELECT username from users")
                res = cur.fetchall()
            with pyodbc.connect(cnxn) as db:
                cur = db.cursor()
                cur.execute("SELECT email from users")
                resE = cur.fetchall()
            for i in range(len(res)):
                if uname == res[i][0]:
                    errorFlag = 1
                    break
            for i in range(len(resE)):
                if email == resE[i][0]:
                    errorFlag = 2
                    break
            if errorFlag == 1:
                statBar.bell()
                statBar.configure(bg="red",relief=Tk.RAISED,text="USERNAME ALREADY EXISTS, ENTER A DIFFERENT USERNAME")
                self.enterUname.delete(0,Tk.END)
            if errorFlag == 2:
                statBar.bell()
                statBar.configure(bg="red",relief=Tk.RAISED,text="EMAIL-ID ALREADY IN USE FOR ANOTHER USER, ENTER A DIFFERENT EMAIL-ID")
                self.enterEmail.delete(0,Tk.END)
            if errorFlag == 0:
                self.registerUser()

    ### DOES THE ACTUAL REGISTERING AFTER ENSURING EVERYTHING'S RIGHT ####

    def registerUser(self):
        u = self.enterUname.get()
        p = self.enterpass.get()
        e = self.enterEmail.get()
        with pyodbc.connect(cnxn) as db:
            try:
                cur = db.cursor()
                cur.execute("INSERT INTO users (username,pwd,email) VALUES (?,?,?)",(u,p,e,))
                statBar.configure(bg="green",relief=Tk.SUNKEN,text="ACCOUNT CONFIGURED! GO BACK AND LOG IN")
            except:
                statBar.bell()
                statBar.configure(bg="red",relief=Tk.RAISED,text="AN ERROR OCCURED, CHECK YOUR INTERNET CONNECTION AND RETRY")

    def reset(self):
        self.master.title("SIGN UP !")
        statBar.configure(bg="black",text="New User Details",relief = Tk.SUNKEN)
        self.enterUname.delete(0,Tk.END)
        self.enterEmail.delete(0,Tk.END)
        self.enterpass.delete(0,Tk.END)
        self.enterpass2.delete(0,Tk.END)

    def tkraise(self):
        self.reset()
        Tk.Frame.tkraise(self)


root = Tk.Tk()
#root.state('zoomed')
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
for frame in (loginWin, startWin, signupWin):
    frame.grid(row=0, column=0, sticky='news')
startWin.tkraise()
root.mainloop()
