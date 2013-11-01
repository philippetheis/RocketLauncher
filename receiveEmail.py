#!/usr/bin/python

#imports for email
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate
from email import Encoders

USERNAME = "treibaufrocketlauncher@gmail.com"     #your gmail
PASSWORD = "jenkinsrocket" 			#your gmail password	

##########################################
#FUNCTION TO GET UNREAD EMAILS	
##########################################

def check_email_get_targets():
    status, email_ids = imap_server.search(None, '(UNSEEN)')
    if email_ids == ['']:
        print('No Unread Emails')
        targets_list = []
    else:
        for e_id in email_ids[0].split():   		      
    	resp, data = imap_server.fetch(e_id, '(RFC822)')   
        perf = HeaderParser().parsestr(data[0][1])	      
        print('Perf: ' , perf)
    	targets_list.append(perf['To'])		          
        print('List of Targets: ', targets_list)

    imap_server.close()
    return targets_list


if __name__ == '__main__':
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
    imap_server.login(USERNAME, PASSWORD)
    imap_server.select('INBOX')
    target_list = check_email_get_targets()
    if target_list :
        print("I got an email")
    else:
        print("I got no email")

