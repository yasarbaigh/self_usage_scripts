import smtplib

#python 2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from email.mime.text import MIMEText



class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message_with_attach(self, to, subject, body, attachment_file_url, attachment_file_name ):
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = to

        msg.attach(MIMEText(body, 'plain'))   
        
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment_file_url, "rb").read())
        Encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename="' + attachment_file_name + '"')

        msg.attach(part)
        
        
        self.session.sendmail(
            self.email,
            to,
            msg.as_string())
        
        print("Successfully sent mail. ")
        
        
    def send_message(self, to, subject, body):
        
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + to,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            to,
            headers + "\r\n\r\n" + body)
        print("Successfully sent mail. ")


gm = Gmail('myemail@gmail.com', 'passwordids@123$')

#gm.send_message('myemail@gmail.com', 'From Tech -Test', 'Message')

gm.send_message_with_attach('myemail@gmail.com', 'Subject From Tech -Test ' , 'Body Attaching reports' , "/tmp/reports.tsv.zip" , "reports.tsv.zip")


