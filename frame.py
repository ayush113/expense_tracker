import Tkinter as Tk
import sqlite3
import tkMessageBox

database = "Accounts.db"

#### THE ACCOUNT DISPLAY CLASS

class accDetails(Tk.Frame):

    def __init__(self,master):

        Tk.Frame.__init__(self,master,bg="#21618c")
        self.master.title("CHANGE YOUR ACCOUNT DETAILS")




        self.pChange = Tk.Button(self,text="Change Password",font=('Calibri', 18),
        fg="#f4d03f", bg="#424949",activebackground="#797d7f",command=self.changepass)

        self.eChange = Tk.Button(self,text="Change Email ID",font=('Calibri', 18),
        fg="#f4d03f", bg="#424949",activebackground="#797d7f",command=self.changemail)

        self.Delete = Tk.Button(self,text = "DELETE ACCOUNT",font=('Britannic Bold',20)
        ,fg="#000000",bg="#ff0000",activebackground="#797d7f",command=self.deleteAccount)

        for row in range(18):
            self.rowconfigure(row,weight=1)
        for col in range(7):
            self.columnconfigure(col,weight=1)



        self.pChange.grid(row=3,column=3,rowspan=1,sticky="news")
        self.eChange.grid(row=9,column=3,rowspan=1,sticky="news")
        self.Delete.grid(row=15,column=3,rowspan=1,sticky="news")


    def changepass(self):
        global child
        child = Tk.Tk()
        currPlabel = Tk.Label(child,text="Current Password",justify=Tk.RIGHT)
        changePlabel = Tk.Label(child,text="New Password",justify=Tk.RIGHT)
        global currPentry
        global changePentry
        currPentry = Tk.Entry(child,relief=Tk.SUNKEN)
        changePentry = Tk.Entry(child,relief=Tk.SUNKEN)
        submitBn = Tk.Button(child,text="SUBMIT",relief=Tk.RAISED,command=self.CP)


        for row in range(7):
            child.rowconfigure(row,weight=1)
        for col in range(4):
            child.columnconfigure(col,weight=1)

        currPlabel.grid(row=2,column=1,sticky="news")
        changePlabel.grid(row=4,column=1,sticky="news")
        currPentry.grid(row=2,column=3,sticky="news")
        changePentry.grid(row=4,column=3,sticky="news")
        submitBn.grid(row=6,column=2,sticky="news")

        child.mainloop()

    def changemail(self):
        global child2
        child2 = Tk.Tk()
        currPlabel = Tk.Label(child2,text="Current Password",justify=Tk.RIGHT)
        maillabel = Tk.Label(child2,text="New Email ID",justify=Tk.RIGHT)
        global currPentry1
        global mailentry1
        currPentry1 = Tk.Entry(child2,relief=Tk.SUNKEN)
        mailentry1 = Tk.Entry(child2,relief=Tk.SUNKEN)
        submitBn = Tk.Button(child2,text="SUBMIT",relief=Tk.RAISED,command=self.CE)


        for row in range(7):
            child2.rowconfigure(row,weight=1)
        for col in range(4):
            child2.columnconfigure(col,weight=1)

        currPlabel.grid(row=2,column=1,sticky="news")
        maillabel.grid(row=4,column=1,sticky="news")
        currPentry1.grid(row=2,column=3,sticky="news")
        mailentry1.grid(row=4,column=3,sticky="news")
        submitBn.grid(row=6,column=2,sticky="news")

        child2.mainloop()


    def deleteAccount(self):
        #### CODE TO BE ADDED
        global subject
        subject = Tk.Tk()
        label = Tk.Label(subject,text="Enter your Password",justify = Tk.RIGHT)
        global labelEntry
        labelEntry = Tk.Entry(subject,relief = Tk.SUNKEN)
        submitBn = Tk.Button(child2,text="SUBMIT",relief=Tk.RAISED,command=self.DA)




        ##### CODE TO BE ADDED

    def CP(self):
        pwd = currPentry.get()
        newPwd = changePentry.get()
        if(pwd == "password"):
            with sqlite3.connect(database) as db:
                cur = db.cursor()
                cur.execute("UPDATE users SET pwd = ? WHERE userid = ?",(newPwd,user.user_id,))
                child.destroy()
                tkMessageBox.showinfo("SUCCESS!","Password was changed successfully")

        else:
            tkMessageBox.showinfo("INVALID PASSWORD","Please enter your current password first")
            changePentry.delete(0,Tk.END)
            currPentry.delete(0,Tk.END)

    def CE(self):
        pwd = currPentry1.get()
        newMail = newEmailentry.get()
        ##### Use the validate email functions from class SignupWin in beta.py
        #### I don't know how to , maybe just copy and paste


    def DA(self):
        pwd = labelEntry.get()
        if(pwd==user.pwd):
            with sqlite3.connect(database) as db:
                cur = db.cursor()
                cur.execute("DELETE FROM users,purchases WHERE userid = ?",(user.user_id,))
            subject.destroy()
            tkMessageBox.showinfo("Completed","Your account and all related information has been deleted")
        else:
            subject.destroy()
            tkMessageBox.showinfo("FAILURE!","You are not authorised to delete this account")
        



root = Tk.Tk()
root.state('zoomed')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
acc = accDetails(root)
acc.grid(row=0,column=0,sticky="news")
acc.tkraise()

root.mainloop()
