import smtplib



#python 3
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
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

    def python3_send_message_with_attach(self, to, subject, body, attachment_file_url, attachment_file_name ):
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = to
        
        msg.attach(MIMEText(body, 'plain'))        
        
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment_file_url, "rb").read())
       
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename="' + attachment_file_name + '"')

        msg.attach(part)
                
        
        self.session.sendmail(
            self.email,
            to,
            msg.as_string())
        
        print("Successfully sent mail. ")
        
        
    def python3_send_message(self, to, subject, body):
        ''' This must be removed '''
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

#gm.python3_send_message('myemail@gmail.com', 'From Tech -Test', 'Message')

gm.python3_send_message_with_attach('myemail@gmail.com', 'From Tech -Test -reports' , ' Attaching reports' , "/home/yasar/Desktop/Zrda/py-scripts/fo07JAN2020bhav.csv.zip" , 'fo07JAN2020bhav.csv.zip')



