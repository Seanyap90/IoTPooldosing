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
import requests

def send_alert_sms(pH, FC):
    #connect to textbelt API to send sms
    today = time.strftime("%A")
    
    sean = 'phone_number_1'
    life_guard = 'phone_number_2'

    if (pH > 7.8 and FC <= 3 and FC >= 1):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', pH is HIGH: ' + str(pH),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", pH is HIGH: " + str(pH)
    elif (pH < 7.2 and FC <= 3 and FC >= 1):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', pH is LOW: ' + str(pH),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", pH is LOW: " + str(pH)
    elif (pH <= 7.8 and pH >= 7.2 and FC > 3):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', FC is HIGH: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })        
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", FC is HIGH: " + str(FC)
    elif (pH <= 7.8 and pH >= 7.2 and FC < 1):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', FC is LOW: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", FC is LOW: " + str(FC)
    elif (pH > 7.8 and FC > 3):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', pH is HIGH: ' + str(pH) + ', and FC is HIGH: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", pH is HIGH: " + str(pH) + ", and FC is HIGH: " + str(FC)
    elif (pH > 7.8 and FC < 1):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time_sms) + ' ' + str(time_sms_hour)+ ', pH is HIGH: ' + str(pH) + ', and FC is LOW: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", pH is HIGH: " + str(pH) + ", and FC is LOW: " + str(FC),
    elif (pH < 7.2 and FC > 3):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', pH is LOW: ' + str(pH) + ', and FC is HIGH: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At "+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", pH is LOW: " + str(pH) + ", and FC is HIGH: " + str(FC)
    elif (pH <7.2 and FC < 1):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', pH is LOW: ' + str(pH) + ', and FC is LOW: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })
        #msg["Subject"] = "[ALERT] At " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", pH is LOW: " + str(pH) + ", and FC is LOW: " + str(FC)
    elif (pH <7.2 and FC < 1):
        req = requests.post('https://textbelt.com/text', {
        'phone': life_guard,
        'message': '[ALERT] At'+ str(time.strftime("%Y-%m-%d %H:%M:%S")) + ', pH is LOW: ' + str(pH) + ', and FC is LOW: ' + str(FC),
        'key': '02fb5e0123e33a1e4dd7ab8327d33a2bae5ca789wTN2BM8HR1QLCc0cNAknVkWit'
        })


    print req.json()
    print 'alert sms sent'

#==============================================================
def send_daily_email():
    today = time.strftime("%A")
    
    #emailfrom = "thanhson160198@gmail.com"
    emailfrom = "dosautosg@gmail.com"
    #emailto = "sean.sq.yap@gmail.com"
    #emailto = "thanhson16198@gmail.com"
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
