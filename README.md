# IoT for Swimming Pool Chemical Maintenance
*Strictly not for any public distribution.
This describes the system architecture for a IoT-based system for automated chemical maintenance.  Instead of a menial worker throwing chlorine or trying to fiddle with industrial water treatment equipment such as dosing pumps and water sensors, this system does this accordingly

## Hardware involved
- Any microprocessor such as a Raspberry pi
- pH and ORP probes from Atlas Scientific or any other brand as long as the probes are terminated by BNC.
- USB carrier boards from Atlas Scientific for the raspberry pi interface with the pH and ORP sensors
- Mechanical relays or solid state relays
- LED lights
- Dosing pumps (optional - dependent on swimming pool plant rooms)
- Routers and repeaters*

*dependent on available networking infrastructure at the swimming pool.

## Hardware System Setup
1. Sensors

Both probes and their corresponding reading chips are required:
- https://atlas-scientific.com/ezo-ph-circuit/
- https://atlas-scientific.com/ezo-orp-circuit/

2. Actual System - Microprocessor and Pump actuation
<img width="849" alt="dosauto" src="https://user-images.githubusercontent.com/34641712/132083613-ce6f88af-20b0-47fe-b997-8294d480abd7.PNG">

## Deployment Examples
1.  Microprocessor, sensors and pump actuation all hardwired in 1 system
2.  Separate sub-systems - Microprocessor and sensors at pool side and pump actuation in a plant room.  Wifi communication between these systems.

<img width="397" alt="deployment" src="https://user-images.githubusercontent.com/34641712/132083648-c32bd120-d341-4510-b0e2-5213523a1635.PNG">

## Software/Middleware Setup
APIs/libraries required:
- Plotly - to display graphs on webapp dashboard
- Textbelt - send SMS
- Dataplicity - remote access to the system
- Flask

*Ideally should have a requirements.txt file for easy installation
![DosAuto IoT System diagram](https://user-images.githubusercontent.com/34641712/166080352-e57188c2-36ef-4342-8b78-36c7e9981c4f.png)



## Web app
Dashboard view and Pump control view:

![image](https://user-images.githubusercontent.com/34641712/132084881-2ee7b379-e504-4683-8a19-0bebfd6f624b.png)
![image](https://user-images.githubusercontent.com/34641712/132084888-ebc39eae-822e-4b7c-805a-586ffe447898.png)

## Dosing.py
• Purpose: Gather sensor data, plot sensor data hourly and decide whether chlorine is needed at the pool every hour.
• Function:
  1. Pre-initialisation; importing sms_gmail_alert.py, graph.py and backup_files_email.py
  2. Initialisation to inform that the device is about the start
  3. Function to derive chlorine values at corresponding pH value;
  4. the main code to hourly retrieve and analyse sensor values to determine whether the pool needs an injection of chlorine
  5. Main code activates sms_gmail_alert.py, graph.py and backup_files_email.py based on the sensor values and scheduled system backups.

## App.py
• Purpose: Allow user to view the pH and Chlorine values on a custom interface while giving the user the option to switch between automatic and manual mode. That means switching between python and HTML scripts.
• Function:
  1. Initialisation – Import Flask, render template, import subprocess
  2. Created a dictionary to attach name and state to digital i/o pins
  3. Two functions for declaration of auto mode and manual mode
  4. Main code: Divided into a few actions: login page, default mode, change to manual and change to auto, update amount of minutes of chlorination left during manual mode when      user relogins

## Crontab.txt
Copy the commands in this txt file into crontab for automatic and headless running of code
