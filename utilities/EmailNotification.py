from email.message import EmailMessage
import ssl
import smtplib


def EmailNotify(receiver:str, subject:str, body:str):
    try:
        email_sender = "toluondrums@gmail.com"
        email_password = "elnm sfgs atad egvw"
        email_receiver = receiver

        subject = subject

        body = f"""{body}"""

        emailObj = EmailMessage()
        emailObj['From'] = email_sender
        emailObj['To'] = email_receiver
        emailObj['subject'] = subject
        emailObj.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, emailObj.as_string())
            return "Notification Successful"
    except Exception as ex:
        return ex
    
receiver = "oladokun7141@gmail.com"
subject = "RETEST ACTIVATED!!!"
body = "TOLUWALASE IS RETESTING THIS SERVICE AGAIN"

# result = EmailNotify(receiver, subject, body)
# print(result)