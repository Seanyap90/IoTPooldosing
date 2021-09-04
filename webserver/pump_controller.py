#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import csv

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

start_time_1 = 0
timer1 = 0
start_time_2 = 0
timer2 = 0
time.sleep(10)

#Communication
TCP_IP = ""
TCP_PORT = 12345
BUFFER_SIZE = 1024

with open('/home/pi/pins_status.csv', 'r') as inp:
   reader = csv.reader(inp, delimiter='\t')
   status = list(reader)

print 'status =' + str(status)
print str(status[0][0])
print str(status[1][0])

def write_to_file(content):
   cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
   #Open the file to write received data
   with open('/home/pi/acknowledged.csv', 'ab') as out:
      writer = csv.writer(out, delimiter='\t', dialect='excel')
      writer.writerow([cur_time, content])

def send_msg(text):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(60)   #timeout 1 mins
	
   for i in range(1):
      TCP_IP = "10.10.8.149"
      try:
         s.connect((TCP_IP, TCP_PORT))
         s.send(text)
         data = s.recv(BUFFER_SIZE)	#Receive the echo
         s.close()

         print "received data:", data
         if str(text) == str(data):
            write_to_file(str(data))
         else:
            write_to_file('ConnectionError')
                
         return "Successfully sent."
      except socket.timeout:
         write_to_file("TimeoutError")
         email_gmail.send_email_communication_error('TimeoutError')
      except:
         write_to_file("UnexpectedError")
         email_gmail.send_email_communication_error('Unexpected Error')
         
   return "Lost connection with dosing."

def save_status(changePin):
   changePin = int(changePin)

   with open('/home/pi/pins_status.csv', 'rb') as inp:
      reader = csv.reader(inp, delimiter ='\t')
      arr = list(reader)
      if changePin == 16:
         new_arr = ['0', str(arr[1][0])]
      elif changePin == 11:
         new_arr = [str(arr[0][0]), '0']

   with open('/home/pi/pins_status.csv','wb') as out:
      writer = csv.writer(out, delimiter ='\t')
      writer.writerow([str(new_arr[0])])
      writer.writerow([str(new_arr[1])])


while True:
   with open('/home/pi/pins_status.csv', 'r') as inp:
      reader = csv.reader(inp, delimiter='\t')
      status = list(reader)

   try:
      #Pump1 timer
      if int(status[0][0]) > 0 and start_time_1 == 0:
         #start_time_1 = int(status[0][0])
         timer1 = time.time()

      if start_time_1 < int(status[0][0]):
         start_time_1 += time.time() - timer1
         timer1 = time.time()
      elif start_time_1 > int(status[0][0]):
         timer1 = 0
         start_time_1 = 0
         GPIO.output(16, GPIO.LOW)
         send_msg('16_0')
         print "Pump1 stopped."
         save_status(16)

      #Pump2 timer
      if int(status[1][0]) > 0 and start_time_2 == 0:
         timer2 = time.time()

      if start_time_2 < int(status[1][0]):
         start_time_2 += time.time() - timer2
         timer2 = time.time()
      elif start_time_2 > int(status[1][0]):
         timer2 = 0
         start_time_2 = 0
         GPIO.output(11, GPIO.LOW)
         send_msg('11_0')
         print "Pump2 stopped."
         save_status(11)

   except:
      pass
