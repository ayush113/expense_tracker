class Purchase(object): #class for single purchase
    def __init__(self,desc,price,locID,catID,date):
        self.desc=desc
        self.price=price
        self.locID=locID
        self.catID=catID
        self.date=date
        
class User(object):     #class for single user
    def __init__(self, purchaseID, userID, userName, pwd, question, ans):
        self.purchaseID=purchaseID
        self.userID=userID
        self.userName=userName
        self.pwd=pwd
        self.question=question
        self.ans=ans

    def create(self):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO users(userName,pwd,question,ans) VALUES (%s,%s,%s,%s)" % (self.userName,self.pwd,self.question,self.ans))
            db.commit()

    def edit(self):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE users SET userName=%s, pwd=%s, question=%s, ans=%s WHERE userID=%d" % (self.userName, self.pwd, self.question, self.ans))
            db.commit()
            
    def delete(self):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM users WHERE userID = %d" % (self.userID,))
            db.commit()
    
    def insert_expense(self,purchase):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("INSERT INTO purchases(userID, desc, catID, locID, date, price) VALUES (%d,%s,%d,%d,%s,%f)" % (self.userID, purchase.desc, purchase.catID, purchase.locID, purchase.date, purchase.price))
            db.commit()

    def edit_expense(self, purchase):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("UPDATE purchases SET userID=%d, desc=%s, catID=%d, locID=%d, date=%s, price=%f WHERE purchaseID=%d" % (self.userID, purchase.desc, purchase.catID, purchase.locID, purchase.date, purchase.price, purchase.purchaseID))
            db.commit()

    def delete_expense(self, purchase):
        with sqlite3.connect(db_name) as db:
            cur=db.cursor()
            cur.execute("DELETE FROM purchases WHERE purchaseID=%d" % (purchase.purchaseID,))
            db.commit()
