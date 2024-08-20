#!/usr/bin/python
import serial # required for communication with boards
import RPi.GPIO as GPIO
from time import strftime # used for timestamps
from time import sleep
from math import exp, expm1
import plotly.plotly as py
from plotly.graph_objs import *
from plotly import tools
from plotly.tools import FigureFactory as FF
import csv
import math
from serial.serialutil import SerialException
import time
import sys
import socket
import sys
from graph import make_table, make_line
import backup_files_email
import sms_gmail_alert

#==============================================================================
#Initualize the serial ports
usbport1 = '/dev/ttyUSB0'
usbport2 = '/dev/ttyUSB1'
ser1 = serial.Serial(usbport1, 9600, timeout = 0) # sets the serial port to the specified port, with a 9600 baud rate
ser2 = serial.Serial(usbport2, 9600, timeout = 0)
sleep(0.5)
ser1.close()
ser2.close()
sleep(1)
#==============================================================================
#declaration of variables, initialisation of usbports for serial communication
usbport1 = '/dev/ttyUSB0'
usbport2 = '/dev/ttyUSB1'
ser1 = serial.Serial(usbport1, 9600, timeout = 0) # sets the serial port to the specified port, with a 9600 baud rate
ser2 = serial.Serial(usbport2, 9600, timeout = 0)
line_ph = " "
line_orp= " "
phArray = []
orpArray = []
a = 0
b = 0
i = 0
j = 0
z = 0
pump_start_time = 0
analysis_ctrl = 0
ser1.write("\r")
ser1.write("C,1\r")
ser2.write("\r")

#Communication
TCP_IP = ""
TCP_PORT = 12345
BUFFER_SIZE = 1024

# Declaration of GPIO pins of raspberry pi to provide digital signals to led lights and mechanical relays connected to pumps
# GPIO 36, 38, 40 - indicative lights to show various states of operation
# GPIO 11, 16 - switch on and off mechanical relays for pumps
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
state1 = GPIO.input(36)
state2 = GPIO.input(38)
state3 = GPIO.input(40)
state4 = GPIO.input(16)
state5 = GPIO.input(11)

#=============================================================================
# definition of funtions, especially free chlorine derivation
# free chlorination derivation from ORP and pH readings
def derive():
    print (strftime("%H:%M"))
    ph = round(float(avg_ph), 3)	# 3 decimals
    print ph
    orp = round(float(avg_orp), 3)	# 3 decimals
    print orp
    hypo_acid = round(exp((orp-771.15)/40.582), 3)
    if 6.0<= ph <= 9.0:
        if (ph == 6.0):
            ratio_fc = 0.95
        elif (ph == 6.1):
            ratio_fc = 0.94
        elif (ph == 6.2):
            ratio_fc = 0.93
        elif (ph == 6.3):
            ratio_fc = 0.92
        elif (ph == 6.4):
            ratio_fc = 0.91
        elif (ph == 6.5):
            ratio_fc = 0.90
        elif (ph == 6.6):
            ratio_fc = 0.88
        elif (ph == 6.7):
            ratio_fc = 0.86
        elif (ph == 6.8):
            ratio_fc = 0.83
        elif (ph == 6.9):
            ratio_fc = 0.77
        elif (ph == 7.0):
            ratio_fc = 0.75
        elif (ph == 7.1):
            ratio_fc = 0.72
        elif (ph == 7.2):
            ratio_fc = 0.67
        elif (ph == 7.3):
            ratio_fc = 0.62
        elif (ph == 7.4):
            ratio_fc = 0.55
        elif (ph == 7.5):
            ratio_fc = 0.5
        elif (ph == 7.6):
            ratio_fc = 0.44
        elif (ph == 7.7):
            ratio_fc = 0.40
        elif (ph == 7.8):
            ratio_fc = 0.31
        elif (ph == 7.9):
            ratio_fc = 0.25
        elif (ph == 8.0):
            ratio_fc = 0.22
        elif (ph == 8.1):
            ratio_fc = 0.20
        elif (ph == 8.2):
            ratio_fc = 0.17
        elif (ph == 8.3):
            ratio_fc = 0.14
        elif (ph == 8.4):
            ratio_fc = 0.10
        elif (ph == 8.5):
            ratio_fc = 0.08
        elif (ph == 8.6):
            ratio_fc = 0.06
        elif (ph == 8.7):
            ratio_fc = 0.05
        elif (ph == 8.8):
            ratio_fc = 0.04
        elif (ph == 8.9):
            ratio_fc = 0.016
        elif (ph == 9.0):
            ratio_fc = 0.03
        else:
            print("out of range...")
            return "imbalance"

        free_chlorine = (hypo_acid)/(ratio_fc)
        free_chlorine = "%.2f" %free_chlorine
        print(free_chlorine)
        return free_chlorine

    else:
        print("check chemicals")
        free_chlorine = 0.0
        return free_chlorine
    return free_chlorine
#==============================================================================
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
         return "Successfully sent."
      except socket.timeout:
         try:
            backup_files_email.send_email_communication_error('TimeoutError')
         except:
            print "Cannot send Alert email."
         print "TimeoutError"
      except Exception as exc:
         print exc
         try:
            backup_files_email.send_email_communication_error('Unexpected Error')
         except:
            print "Cannot send Alert email."
         print "ConnectionError"

   return "ConnectionError"
#==============================================================================
#initialise with zero input for all GPIO signals - pumps and led lights to start from "OFF" state
if (state1 == True) or (state2 == True) or (state3 == True) or (state4 == True) or (state5 == True):
    GPIO.output(36,False)
    GPIO.output(38,False)
    GPIO.output(40,False)
    GPIO.output(16,False)
    GPIO.output(11,False)
    print("OFF")

print("FutureRemedy Labs"+"\n")
print("DosAuto System Ready")
print("Time now:" + strftime("%H:%M:%S"))

#Variable to stop the pump if exceed time
cur_hour = int(strftime("%H")) -1

#==============================================================================
#main code
while True:
    today = strftime('%A')
    #polling from pH and ORP sensors
    if (state1 == False):
        GPIO.output(36,True)
        state1 = True

    try:
        data_ph = ser1.read()
    except:
        data_ph = '-1'

    if (data_ph == "\r"):
        try:
            line_ph = float (line_ph)
            phArray.append(line_ph)
        except ValueError:
            pass
        line_ph = " "
    elif data_ph != '-1':
        line_ph = line_ph + data_ph

    try:
        data_orp = ser2.read()
    except:
        data_orp = '-1'

    if (data_orp == "\r"):
        try:
            line_orp = float (line_orp)
            orpArray.append(line_orp)
        except ValueError:
            pass
        line_orp = " "
    elif data_orp != '-1':
        line_orp = line_orp + data_orp


    #getting average of 10 recorded sensor values
    if (len(phArray)== 10 and len(orpArray) == 10):
        avg_ph = sum (phArray)/float (len(phArray))
        avg_ph = (float (avg_ph) - 0.5)
        avg_ph = "%.1f" % avg_ph
        avg_orp = sum(orpArray)/float (len(orpArray))
        final_orp = "%.1f"%avg_orp
        
        # get free chlorine values
        free_chlorine = derive()
        
        if (state1 == True):
            GPIO.output(36,False)
            state1 = False
            sleep(1)

        #record pH and chlorine data into csv
        #switch on indicative light
        try:
            update = int(strftime("%M"))
            if (update%5 == 0):
                if (state2 == False):
                    GPIO.output(38,True)
                    state2 = True
                    sleep(1.5)
                at_time = strftime("%Y-%m-%d %H:%M:%S")
                system_time = int(round(time.time()*1000))
                ph_upper = 7.6
                ph_lower = 7.2
                cl_upper = 3
                cl_lower = 1
                print("backup")
                csv_out = open('/home/pi/Desktop/' + today + '.csv', 'a')
                mywriter = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                mywriter.writerow([system_time, at_time, avg_ph, final_orp, free_chlorine, ph_upper, ph_lower, cl_upper, cl_lower])
                csv_out.close()
                if (state2 == True):
                    GPIO.output(38,False)
                    state2 = False
                    sleep(1.5)
        except ValueError:
            pass

	# Get pumps to start dosing
        if (6<= int(strftime("%H"))  <= 18) and int(strftime("%H"))!= cur_hour and int(strftime("%M"))>=59:
            GPIO.output(16,False)
            state4 == False
            GPIO.output(11,False)
            state5 == False
            GPIO.output(40,False)
            state3 = False
            sleep(0.5)
            print ("dose done")
            pump_start_time = 0
            send_msg('reset_auto')
            cur_hour = int(strftime("%H"))
        elif (int(strftime("%H")) > 18 or int(strftime("%H")) < 6) and int(strftime("%H"))!= cur_hour and int(strftime("%M"))>=59:
            GPIO.output(16,False)
            state4 == False
            GPIO.output(11,False)
            state5 == False
            GPIO.output(40,False)
            state3 = False
            sleep(0.5)
            print ("dose done")
            pump_start_time = 0
            send_msg('reset_auto')
            cur_hour = int(strftime("%H"))
        else:
            pump_start_time = 0

        # Every hour, sensor values will decide whether to stop dosing or continue
        if (float(strftime("%M")) == 1 and (analysis_ctrl == 0)):
            
            # dosing settings for day time
            if (7<= int(strftime("%H"))  <= 18):
                print("daytime dose")
                if (float(avg_ph)<=7.8) and (0<=float(free_chlorine)<=1):		
                    # dose since chlorine is at lower limits of acceptable range
                    # activate pump
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 1
                        safety = 0
                        print("backup")
                        
                        # edit system log
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                    except ValueError:
                        pass
                    print("switch on")
                    
                    # switch on alert system lights and continue pump to dose since there is low levels of chlorine
                    GPIO.output(40,True)
                    state3 = True
                    GPIO.output(16,True)
                    state4 == True
                    GPIO.output(11,True)
                    state5 == True
                    
                    # activate alert system
                    try:
                        backup_files_email.send_alert_email('Chlorine is too low')
                    except:
                        print 'Cannot send alert email: Chlorine is too low.'
                    try:
                        sms_gmail_alert.send_alert_sms(float(avg_ph), float(free_chlorine))
                    except:
                        print 'Cannot send alert sms: Chlorine is too low.'
                    
                    # pumping time
                    pump_start_time = time.time()


                elif (float(avg_ph)<=7.8) and (1<float(free_chlorine)<=2.5):
                    # dose since chlorine is at lower limits of acceptable range
                    # activate pump
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 1
                        safety = 1
                        print("backup")
                        
                        # update system log
                        csv_out = open('/home/pi/Desktop/'+ today + '_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                    except ValueError:
                        pass
                    print("switch on")
                    
                    # swithch on led alert system and continue dosing pumps
                    GPIO.output(40,True)
                    state3 = True
                    GPIO.output(16,True)
                    state4 == True
                    GPIO.output(11,True)
                    state5 == True
                    pump_start_time = time.time()


                elif (7.2<=float(avg_ph)<=7.8) and (2.5<float(free_chlorine)<=3.0):
                    # do nothing because chemicals are in acceptable range
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 0
                        safety = 1
                        print("backup")
                        
                        # update system log
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                        pump_start_time = time.time()
                    except ValueError:
                        pass
                    
                    # switch off dosing while alert system remains inactive
                    print("not dosing this hour")
                    print("switch off")
                    GPIO.output(16,False)
                    GPIO.output(11,False)
                    send_msg('off_auto')
                    pump_start_time = time.time()

                else:
                    # do nothing since chemical content are in unacceptable ranges, activate alert system
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 0
                        safety = 0
                        print("backup")
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                        # activate alert system for further action
                        try:
                            backup_files_email.send_alert_email('pH or Chlorine is out of range')
                        except:
                            print 'Cannot send alert email.'
                        try:
                            sms_gmail_alert.send_alert_sms(float(avg_ph), float(free_chlorine))
                        except:
                            print 'Cannot send alert sms: pH or Chlorine is out of range.'

                        send_msg('off_auto')
                        pump_start_time = time.time()
                    except ValueError:
                        pass
                    
                    # stop dosing as there are too much chemicals
                    print("not dosing this hour")
                    print("switch off")
                    GPIO.output(16,False)
                    GPIO.output(11,False)

            else:
                # dosing settings for night time
                print("nighttime dose")
                if (7.2<=float(avg_ph)<=7.8) and (0<=float(free_chlorine)<=1):
                    # dose since chlorine is at lower limits of acceptable range
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 1
                        safety = 0
                        print("backup")
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                    except ValueError:
                        pass
                    print("switch on")
                    GPIO.output(40,True)
                    state3 = True
                    GPIO.output(16,True)
                    state4 == True
                    GPIO.output(11,True)
                    state5 == True
                    try:
                        backup_files_email.send_alert_email('Chlorine is too low')
                    except:
                        print 'Cannot send alert email: Chlorine is too low.'
                    sleep(120)
                    GPIO.output(16,False)
                    state4 == False
                    GPIO.output(11,False)
                    state5 == False
                    GPIO.output(40,False)
                    state3 = False
                    sleep(0.5)
                    #print ("dose done")
                elif (7.2<=float(avg_ph)<=7.8) and (1<float(free_chlorine)<=2.5):
                    #dose since chlorine is at lower limits of acceptable range
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 1
                        safety = 1
                        print("backup")
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                    except ValueError:
                        pass
                    print("switch on")
                    GPIO.output(40,True)
                    state3 = True
                    GPIO.output(16,True)
                    state4 == True
                    GPIO.output(11,True)
                    state5 == True
                    sleep(120)
                    GPIO.output(16,False)
                    state4 == False
                    GPIO.output(11,False)
                    state5 == False
                    GPIO.output(40,False)
                    state3 = False
                    sleep(0.5)
                    #print ("dose done")
                elif (7.2<=float(avg_ph)<=7.8) and (2.5<float(free_chlorine)<=3.0):
                    #do nothing because chemicals are in acceptable range
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 0
                        safety = 1
                        print("backup")
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                    except ValueError:
                        pass
                    print("not dosing this hour")
                    print("switch off")
                    GPIO.output(16,False)
                    GPIO.output(11,False)
                    send_msg('off_auto')

                else:
                    #do nothing since chemicals are in unacceptable ranges
                    try:
                        if (state2 == False):
                            GPIO.output(38,True)
                            state2 = True
                            sleep(1.5)
                        at_time = strftime("%Y-%m-%d %H:%M:%S")
                        system_time = int(round(time.time()*1000))
                        dose = 0
                        safety = 0
                        print("backup")
                        csv_out = open('/home/pi/Desktop/'+ today +'_dose_record.csv', 'a')
                        b_writer = csv.writer(csv_out, delimiter = '\t', dialect = 'excel')
                        b_writer.writerow([system_time, at_time, dose, safety])
                        csv_out.close()
                        if (state2 == True):
                            GPIO.output(38,False)
                            state2 = False
                            sleep(1.5)
                    except ValueError:
                        pass
                    print("not dosing this hour")
                    print("switch off")
                    send_msg('off_auto')
                    try:
                        backup_files_email.send_alert_email('pH or Chloride is in unacceptable range.')
                    except:
                        print 'Cannot send alert email: pH or Chloride is in unacceptable range.'
                    GPIO.output(16,False)
                    GPIO.output(11,False)

            #control variable activated
            analysis_ctrl = 1
            print 'analysis_ctrl =', analysis_ctrl
            print ("control variable activated")

            #plotly upload
            analysis_csv = int(round(time.time()*1000))
            #print analysis_csv
            print 'trying to upload to Plotly'
            try:
                host = "8.8.8.8"
                port = 53
                socket.setdefaulttimeout(1)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host,port))
                print("connected")

                #Plot line charts and table
                make_table()
                make_line()

            except socket.timeout:
                print 'TimeoutError. Cannot upload to plotly.'
            except Exception:
                print 'Error. Cannot uploadto plotly.'
        #reset control variable before a new hour
        if (int(strftime("%M")) == 59 and analysis_ctrl == 1):
            analysis_ctrl = 0
            print analysis_ctrl
            print ("reset for dosing")
            sleep(0.5)

        #reset arrays
        phArray = []
        orpArray = []
        GPIO.output(16,False)
        GPIO.output(11,False)


    if (len(phArray)> 10 or len(orpArray) > 10):
        phArray = []
        orpArray = []
