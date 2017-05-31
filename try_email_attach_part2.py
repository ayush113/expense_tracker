#!/usr/bin/python
import smtplib
import os
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

print '''

  ________               .__.__   
 /  _____/  _____ _____  |__|  |  
/   \  ___ /     \\__  \ |  |  |  
\    \_\  \  Y Y  \/ __ \|  |  |__
 \______  /__|_|  (____  /__|____/
        \/      \/     \/         
                           File  send
               Coder by jimmyromanticdevil
''' 

gmail_id = raw_input('[+]Enter your account :')
gmail_pass =raw_input('[+]Enter youre password : ')

def mail(to, subject, text, attach):
    
    pesan = MIMEMultipart()

    pesan['From'] = 'Expense Tracker 9000XL'
    pesan['To'] = 'Joshua DCunha <joshdcunha99@gmail.com>'
    pesan['Subject'] = subject

    pesan.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
            'attachment; filename="%s"' % os.path.basename(attach))
    pesan.attach(part)
    server_gmail = smtplib.SMTP("smtp.gmail.com", 587)
    server_gmail.ehlo()
    server_gmail.starttls()    
    server_gmail.ehlo()
    server_gmail.login(gmail_id, gmail_pass)    
    server_gmail.sendmail(gmail_id, to, pesan.as_string())
    server_gmail.close()



more_send="y"
r = []


while more_send == "y":
    recepient_email = raw_input("[+]Email address recepients: ")
    r.append(recepient_email)
    more_send = raw_input("[*]Do you want to send more (y/n): ")

subject = raw_input("[+]Subject: ")
body = raw_input("[+]Body: ")
attachment = raw_input("[+]Enter attachment file path: ")

for email_list in r:
    mail(email_list,subject,body,attachment)
    print "Your email for "+str(email_list)+" was send successfully"

