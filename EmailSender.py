import smtplib
from email.message import EmailMessage

sender = "truonghieu2312@outlook.com.vn"
password = "Nth@23122"
destination = "truonghieu2312@gmail.com"

mailServer = "smtp.office365.com"
port = 587

def SendEmail(subject, body):
    msg = EmailMessage()
    msg["To"] = destination
    msg["From"] = sender
    msg["Subject"] = subject
    msg.set_content(body)

    send = smtplib.SMTP(mailServer, port)
    send.starttls()
    send.login(sender, password)
    send.send_message(from_addr=sender, to_addrs=destination, msg=msg)

#SendEmail("Warning", "Body")