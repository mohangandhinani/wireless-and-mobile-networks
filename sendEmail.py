import smtplib

def sendemail(sender,receiver,cc_addr_list,sub,message,login, password,smtpserver='smtp.gmail.com:587'):
    msgHeader  = 'From: %s\n' % sender
    msgHeader += 'To: %s\n' % ','.join(receiver)
    msgHeader += 'Cc: %s\n' % ','.join(cc_addr_list)
    msgHeader += 'sub: %s\n\n' % sub
    message = msgHeader + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(sender, receiver, message)
    server.quit()
    return problems

#sendemail(sender = 'CSE507ProjectNotifications@gmail.com',receiver = ['prashanths1992@gmail.com'],sub='Fire Alarm Detected',message='Detected 11:11:12',login = 'cse507',password = 'cse507')

