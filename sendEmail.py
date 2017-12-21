import smtplib
#TO DO : test with @cs.stonybrook.edu account.
#temporary code to test the feature of the email functionaity using google SMTP Server
def TestsendEmail(sender,receiver,sub,message,login, password,smtp='smtp.gmail.com:587'):
    msgHeader='From: %s\n' % sender
    msgHeader+='To: %s\n' % ','.join(receiver)
    msgHeader+='sub: %s\n\n' % sub
    message=msgHeader + message
    server=smtplib.SMTP(smtp)
    server.starttls()
    server.login(login,password)
    problems=server.sendmail(sender, receiver, message)
    server.quit()
    return problems

#sendemail(sender = 'CSE507ProjectNotifications@gmail.com',receiver = ['prashanths1992@gmail.com'],sub='Fire Alarm Detected',message='Detected 11:11:12',login = 'cse507',password = 'cse507')

