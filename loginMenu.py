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
