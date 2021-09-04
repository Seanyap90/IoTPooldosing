# IoT for Swimming Pool Chemical Maintenance

## Hardware involved
- Any microprocessor such as a Raspberry pi
- pH and ORP probes from Atlas Scientific or any other brand as long as the probes are terminated by BNC.
- USB carrier boards from Atlas Scientific for the raspberry pi interface with the pH and ORP sensors
- Mechanical relays or solid state relays
- LED lights
- Dosing pumps (optional - dependent on swimming pool plant rooms)
- Routers and repeaters*

## Hardware System Setup
1. Sensor
Need both the probes and their corresponding reading chips:
- https://atlas-scientific.com/ezo-ph-circuit/
- https://atlas-scientific.com/ezo-orp-circuit/

2. Actual System
<img width="849" alt="dosauto" src="https://user-images.githubusercontent.com/34641712/132083613-ce6f88af-20b0-47fe-b997-8294d480abd7.PNG">

3. Deployment Examples
<img width="397" alt="deployment" src="https://user-images.githubusercontent.com/34641712/132083648-c32bd120-d341-4510-b0e2-5213523a1635.PNG">

## Software/Middleware Setup
APIs required:
- Plotly - to display graphs on webapp dashboard
- Textbelt - send SMS
- Dataplicity - remote access to the system

![systemarch](https://user-images.githubusercontent.com/34641712/132084848-725e713a-3f27-4c4b-877b-c755f2443051.png)

## Web app
![image](https://user-images.githubusercontent.com/34641712/132084881-2ee7b379-e504-4683-8a19-0bebfd6f624b.png)
![image](https://user-images.githubusercontent.com/34641712/132084888-ebc39eae-822e-4b7c-805a-586ffe447898.png)
