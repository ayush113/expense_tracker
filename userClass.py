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
            cur.execute("INSERT INTO purchases(userID, desc, cat, loc, date, price) VALUES (?,?,?,?,?,?)",(self.userID, values[0], values[1], values[2], values[4], values[3]))
            db.commit()
        print "\n\t\t\tEXPENSE ADDED!"

    def edit_expense(self,purchaseID,values):   #edits expense details and updates them in database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE purchases SET userID=?, desc=?, cat=?, loc=?, date=?, price=? WHERE purchaseID=?",(self.userID, values[0], values[1], values[2], values[4], values[3], purchaseID))
            db.commit()
        print "\n\t\t\tEXPENSE EDITED!"

    def delete_expense(self,purchaseID):    #deletes expense from database
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM purchases WHERE purchaseID=?",(purchaseID,))
            db.commit()
        print "\n\t\t\tEXPENSE DELETED!"
