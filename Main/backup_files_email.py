import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import time

def send_all_in_email():
    emailfrom = "thanhson160198@gmail.com"
    #emailto = "sean.sq.yap@gmail.com"
    emailto = "thanhson16198@gmail.com"
    username = "thanhson160198@gmail.com"
    password = "son9401545"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Back up CSV files weekly"
    msg.preamble = "Back up CSV files weekly"

    fileToSend = ["/home/pi/Desktop/Monday.csv", "/home/pi/Desktop/Tuesday.csv",
                  "/home/pi/Desktop/Wednesday.csv", "/home/pi/Desktop/Thursday.csv",
              "/home/pi/Desktop/Friday.csv", "/home/pi/Desktop/Saturday.csv",
                  "/home/pi/Desktop/Sunday.csv"]
        
    for each_file in fileToSend:
        ctype, encoding = mimetypes.guess_type(each_file)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(each_file)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(each_file, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(each_file, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(each_file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=each_file)
        msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    print 'email sent'

def send_daily_email():
    today = time.strftime("%A")
    
    #emailfrom = "thanhson160198@gmail.com"
    emailfrom = "dosautosg@gmail.com"
    #emailto = "sean.sq.yap@gmail.com"
    emailto = "dosautosg@gmail.com"
    fileToSend = '/home/pi/Desktop/' + today + ".csv"
    username = "dosautosg@gmail.com"
    password = "ASDFrewq1234"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Daily backup CSV"
    msg.preamble = "Daily backup CSV"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    print 'daily email sent'

                     
def send_email_communication_error(error_type):
    today = time.strftime("%A")

    #emailfrom = "thanhson160198@gmail.com"
    emailfrom = "dosautosg@gmail.com"
    #emailto = "sean.sq.yap@gmail.com"
    emailto = "dosautosg@gmail.com"
    fileToSend = '/home/pi/acknowledged.csv'
    username = "dosautosg@gmail.com"
    password = "ASDFrewq1234"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Communication Error: " + error_type +" at " + time.strftime("%Y-%m-%d %H:%M:%S")
    msg.preamble = "Communication Error: " + error_type +" at " + time.strftime("%Y-%m-%d %H:%M:%S")

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    print 'Email about communication error sent.'


def send_alert_email(error_type):
    today = time.strftime("%A")

    #emailfrom = "thanhson160198@gmail.com"
    emailfrom = "dosautosg@gmail.com"
    #emailto = "sean.sq.yap@gmail.com"
    emailto = "dosautosg@gmail.com"
    fileToSend = '/home/pi/Desktop/' + str(today) + '.csv'
    username = "dosautosg@gmail.com"
    password = "ASDFrewq1234"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "CSC Alert: " + error_type +" at " + time.strftime("%Y-%m-%d %H:%M:%S")
    msg.preamble = "CSC Alert: " + error_type +" at " + time.strftime("%Y-%m-%d %H:%M:%S")

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    print 'Alert email sent.'
