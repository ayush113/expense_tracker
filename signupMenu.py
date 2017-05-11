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
