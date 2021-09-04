import socket
TCP_IP = ""
TCP_PORT = 12345
BUFFER_SIZE = 1024

def send_msg(text):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(120)   #timeout 2 mins
	
   for i in range(1):
      TCP_IP = "10.10.8.132"
      if 1>0:
         s.connect((TCP_IP, TCP_PORT))
         s.send(text)
         data = s.recv(BUFFER_SIZE)	#Receive the echo
         s.close()

         print "received data:", data
         return "Successfully sent."
 
send_msg('test')