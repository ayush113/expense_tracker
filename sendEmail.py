import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import glob
import datetime
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
now = datetime.datetime.now()
db_name = "Accounts.db"
_mail = 'expense.trackerxl@gmail.com'

def getMail_gFile():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT email FROM users where userID = ?',(client.userID,))
    res = cur.fetchone()
    fileList = glob.glob('*.pdf')  #Lists all the pdf file at the current location LOOK UP module glob
    print "\t\tCHOOSE ONE OF THE OPTIONS BELOW\t\t"
    print "\n\t\t1. SEND A FILE FORM CURRENT FILES"
    print "\n\t\t2. SEND THE CURRENT MONTH's REPORT"
    print "\n\t\t3. SEND THE CURRENT YEAR's REPORT"
    print "\n\t\t4. QUIT"
    choice = raw_input("Enter your choice\t")
    f = []
    f.append(res[0]) #Stored the current user's email
    if(choice == '1'):
        for i in range(len(fileList)):
            print "%d --->"%(i+1) + "%s"%fileList[i]
        ch = raw_input("Enter the index no. of one of the files from above, Enter 0 to quit\t")
        if(ch == '0'):
            return -1
        else:
            try:
                if(int(ch)<=len(fileList)):
                    f.append(fileList[int(ch)-1])
                else:
                    print "No such index in the list shown.Quitting........"
                    getMail_gFile()
            except:
                print("Invalid input")
                getMail_gFile()
    elif(choice == '2'):
        print "Sending your monthly report for current month"
        month_stats(now.month,now.year)
        fname = 'ayushkumar'+'_'+ months[now.month-1] + '-' + str(now.year) + '.pdf' #Gets the name of the file that should have been there
        sendEmail(f[0],fname)

    elif(choice == '3'):
        print "Press 1 for Stacker bar graph\nPress 2 for pie chart by months"
        ch2 = raw_input()
        if(ch2=='1'):
            year_stats_all(now.year) #Stacked Bar Graph
            fname = client.userName + '_' + str(now.year) + '.pdf'
            sendEmail(f[0],fname)
        elif(ch2 == '2'):
            year_stats_pies(now.year) #Year Pie chart
            fname = client.userName + '_' + str(now.year) + '_Pies.pdf'
            sendEmail(f[0],fname)
        else:
            print "Invalid Input quitting"
            getMail_gFile
    else:
        return -1

def sendEmail(toAddr,_file):
    msg = MIMEMultipart()
    msg['Subject'] = 'EXPENSE-TRACKER XL 9000'
    msg['From'] = _mail
    msg['To'] = toAddr
    msg.attach(MIMEText(raw_input("Enter your Message or Leave Blank")))
    fp = open(_file,'rb')
    att = MIMEApplication(fp.read())
    fp.close()
    att.add_header('Content-Disposition','attachment',filename = _file)
    msg.attach(att)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()  #Sends an extended hello to server
    server.starttls() #starts ttls
    server.ehlo()  # sends hello
    server.login(_mail,"extrack9000")  # FInd a way to store the password in a more secure way
    server.sendmail(_mail,toAddr,msg.as_string())
    server.close()
