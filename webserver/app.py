#!/usr/bin/python
import time
from flask import Flask, render_template, request, redirect
import RPi.GPIO as GPIO
import subprocess
import csv
import socket
import backup_files_email

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)		#Turn off warnings on GPIOs of the RasPi
Auto_mode = None
Manual_mode = None
auto_started = 0
manual_started = 0
auto_is_running = 0
start_sec_1 = 0
start_sec_2 = 0

pump1 = 16
pump2 = 11

#Communication
TCP_IP = ""
TCP_PORT = 12345
BUFFER_SIZE = 1024

def write_to_file(content):
   cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
   #Open the file to write received data
   with open('/home/pi/acknowledged.csv', 'ab') as out:
      writer = csv.writer(out, delimiter='\t', dialect='excel')
      writer.writerow([cur_time, content])
        
def send_msg(text):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(120)   #timeout 2 mins
	
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
         pins[16]['connection_status'] = 1
         return "Successfully sent."
      except socket.timeout:
         write_to_file("TimeoutError")
         backup_files_email.send_email_communication_error('TimeoutError')
         pins[16]['connection_status'] = 0
         print "TimeoutError"
      except Exception as exc:
         write_to_file(str(exc))
         backup_files_email.send_email_communication_error('Unexpected Error')
         pins[16]['connection_status'] = 0
         print "ConnectionError"

   return "ConnectionError"
        
#Create a pins_status.csv
with open('/home/pi/pins_status.csv','wb') as out:
   writer = csv.writer(out, delimiter ='\t')
   writer.writerow(['0'])
   writer.writerow(['0'])

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   16 : {'name' : 'Pin 16', 'timer' :50, 'state' : GPIO.LOW, 'seconds_left': 0, 'connection_status': 1},
   11 : {'name' : 'Pin 11', 'timer' :50, 'state' : GPIO.LOW, 'seconds_left': 0}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

#Set the GPIO for the red LED
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)



def startAuto():
   global Auto_mode
   global auto_started
   global manual_started
   global auto_is_running
   auto_started = 1
   auto_is_running = 1

   send_msg('reset')

def startManual():
   global Manual_mode
   global auto_is_running
   auto_is_running = 0
   print 'auto_is_running set back to 0'
   manual_started = 1
   send_msg('off')

def save_status(changePin):
   changePin = int(changePin)

   with open('/home/pi/pins_status.csv', 'rb') as inp:
      reader = csv.reader(inp, delimiter ='\t')
      arr = list(reader)
      if changePin == pump1:
         new_arr = [str(int(pins[pump1]['timer'])*60), arr[1][0]]
      elif changePin == pump2:
         new_arr = [arr[0][0], str(int(pins[pump2]['timer'])*60)]

   with open('/home/pi/pins_status.csv','wb') as out:
      writer = csv.writer(out, delimiter ='\t')
      writer.writerow([str(new_arr[0])])
      writer.writerow([str(new_arr[1])])

def clear_status():
   with open('/home/pi/pins_status.csv','wb') as out:
      writer = csv.writer(out, delimiter ='\t')
      writer.writerow(['0'])
      writer.writerow(['0'])



@app.route("/")
def main():
   return render_template('login.html');
   
@app.route("/autorun")
def autorun():
   global manual_started

   if (auto_started == 0):
      startAuto()

   #Update the seconds_left
   if start_sec_1 != 0:
      pins[pump1]['seconds_left'] = int(int(pins[pump1]['timer'])*60 - (time.time()-start_sec_1))
   else:
      pins[pump1]['seconds_left'] = 0
   if start_sec_2 != 0:
      pins[pump2]['seconds_left'] = int(int(pins[pump2]['timer'])*60 - (time.time()-start_sec_2))
   else:
      pins[pump2]['seconds_left'] = 0

   if pins[pump1]['connection_status'] == 0:
      return render_template('comm_error.html')
   
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   if auto_is_running == 0:
      return render_template('manual.html', **templateData)
   else:
      return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   global start_sec_1
   global start_sec_2
   
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
      send_msg(str(changePin) + '_' + str(pins[changePin]['timer']))
      save_status(changePin)
      if changePin == pump1:
         start_sec_1 = time.time()
      elif changePin == pump2:
         start_sec_2 = time.time()
         
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
      #Turn the red LED off
      #GPIO.output(40, GPIO.LOW)
      send_msg(str(changePin) + '_0')
      if changePin == pump1:
         start_sec_1 = 0
      elif changePin == pump2:
         start_sec_2 = 0


   #Update the seconds_left
   if start_sec_1 != 0:
      pins[pump1]['seconds_left'] = int(int(pins[pump1]['timer'])*60 - (time.time()-start_sec_1))
   else:
      pins[pump1]['seconds_left'] = 0
   if start_sec_2 != 0:
      pins[pump2]['seconds_left'] = int(int(pins[pump2]['timer'])*60 - (time.time()-start_sec_2))
   else:
      pins[pump2]['seconds_left'] = 0
      
   if pins[16]['connection_status'] == 0:
      return render_template('comm_error.html')
   
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
      
   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }
   return render_template('manual.html', **templateData)

#Change to Automatic mode
@app.route("/<changePin>/auto")
def runAuto(changePin):
   #print 'auto_is_running =', auto_is_running
   if (auto_is_running == 0):
      changePin = int(changePin)	#Converted the input value to integer (int)
      GPIO.output(pump1, GPIO.LOW)		#Pump1
      GPIO.output(pump2, GPIO.LOW)		#Pump2
      GPIO.output(40, GPIO.LOW)		#Red LED
      clear_status()
      pins[pump1]['timer'] = 45
      pins[pump2]['timer'] = 45
      pins[pump1]['seconds_left'] = 0
      pins[pump2]['seconds_left'] = 0
      startAuto()

   if pins[16]['connection_status'] == 0:
      return render_template('comm_error.html')
   
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'pins' : pins
   }
   return render_template('main.html',**templateData)

#Change to Manual mode
@app.route("/<changePin>/manual")
def runManual(changePin):
   changePin = int(changePin)
   startManual()
   auto_started = 0
   GPIO.output(pump1, GPIO.LOW)	#Pump1
   GPIO.output(pump2, GPIO.LOW)	#Pump2
   GPIO.output(40, GPIO.LOW)	#Red LED
   clear_status()
   
   #Update the seconds_left
   if start_sec_1 != 0:
      pins[pump1]['seconds_left'] = int(int(pins[pump1]['timer'])*60 - (time.time()-start_sec_1))
   else:
      pins[pump1]['seconds_left'] = 0
   if start_sec_2 != 0:
      pins[pump2]['seconds_left'] = int(int(pins[pump2]['timer'])*60 - (time.time()-start_sec_2))
   else:
      pins[pump2]['seconds_left'] = 0

   if pins[16]['connection_status'] == 0:
      return render_template('comm_error.html')
   
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'pins' : pins
   }
   return render_template('manual.html',**templateData)

#Change the timer of a pump on web app
@app.route("/<changePin>/timer/<new_timer>")
def setTimer(changePin, new_timer):
   changePin = int(changePin)
   new_timer = int(new_timer)
   GPIO.output(changePin, GPIO.LOW)
   #GPIO.output(40, GPIO.LOW)	#Red LED
   send_msg(str(changePin) + '_0')
   save_status(changePin)
   
   pins[changePin]['seconds_left'] = 0

   if changePin == 16:
      start_sec_1 = 0
   elif changePin == 11:
      start_sec_2 = 0
      
   #Set the new timer for the pump on web app
   pins[changePin]['timer'] = new_timer

   if pins[16]['connection_status'] == 0:
      return render_template('comm_error.html')
   
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'pins' : pins
   }
   return render_template('manual.html', **templateData)

#Return nothing if user misclick 'Save'
@app.route("/<changePin>/timer/")
def false_timer(changePin):
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'pins' : pins
   }
   return render_template('manual.html', **templateData)

#Return the error page when the communication is lost
@app.route("/error/")
def return_comm_error():
   return render_template('comm_error.html')

#Run the webserver
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
