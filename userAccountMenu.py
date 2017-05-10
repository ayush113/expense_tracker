def create_expense(): #function that 'creates' the right expense details before sending them to User method 'add_expense'

    locs=[]
    cats=[]
    descs=[]
    
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
            
        cur.execute("SELECT DISTINCT desc FROM purchases WHERE userID=?", (client.userID,))
        res=cur.fetchall()
        for (desc,) in res:
            descs.append(desc)
        db.commit()
            
    lists=[descs,cats,locs]
    values=[]
    lists2=["description","category","location"]
    
    for i in range(3):  #loop that iteratively stores data about location, category and description w/o rewriting code
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
        values.append(str(timeNow[2])+str(timeNow[1])+str(timeNow[0]))
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
            values.append(str(year)+"-"+str(month)+"-"+str(day))

    return values

def choose_expense():

            #allows the user to pick an expense to edit/delete before sending that
            #expense's purchaseID to User method 'edit_expense'/'delete_expense'
    
    with sqlite3.connect(db_name) as db:
        cur=db.cursor()
        cur.execute("SELECT purchaseID, desc, price, cat, loc, date from purchases WHERE userID=? ORDER BY date desc",(client.userID,))
        res=cur.fetchall()
        db.commit()
    if len(res)!=0:
        ids=[]
        for rec in res:
            ids.append(str(rec[0]))
        print tabulate(res, ["PurchaseID","Description","Price","Category","Location","Date(YYYY-MM-DD)"], tablefmt='grid')
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
        cur.execute("SELECT SUM(price), COUNT(PurchaseID) FROM purchases WHERE userID={0} AND date LIKE '{1}-{2}-%'".format(client.userID, today[0], today[1]))
        res=cur.fetchall()
        monthExpenses=res[0][0]
        monthNo=res[0][1]
        cur.execute("SELECT SUM(price) FROM purchases WHERE userID={0} AND date LIKE '{1}-%'".format(client.userID, today[0]))
        res=cur.fetchall()
        yearExpenses=res[0][0]
        db.commit()
    print "\n\t\t\t\t  %s %s %s %s\n\n\t\t\tEXPENSES THIS MONTH: %.2f\n\t\t\tPURCHASES THIS MONTH: %d\n\t\t\tEXPENSES THIS YEAR: %.2f\n\t\t\tMONTHLY BUDGET: %.2f" % (todate[0], todate[1], todate[2], todate[4], monthExpenses, monthNo, yearExpenses, client.budget)
    
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

        print "\n\t\tIF YOU WANT A DETAIL TO REMAIN AS IS, HIT 0 FOR THAT DETAIL"
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
            
        if userName=='0':
            userName=userNameInp
        if pwd=='0':
            pwd=pwdInp
        if question=='0':
            question==questionInp
        if ans=='0':
            ans=ansInp
        if budget=='0':
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
