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
