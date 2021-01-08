import simplejson as json
import concurrent.futures
import socket
import time

def handleBackupSchedule():
  """Backup schedule using UDP. Listens to backup process writing.py if redis disconnects.
  """
  localIP = "127.0.0.1"
  localPort = 20001
  bufferSize = 1024

  # Create a datagram socket
  UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

  # Bind to address and ip
  UDPServerSocket.bind((localIP, localPort))
  
  # Listen for incoming datagrams
  while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    with concurrent.futures.ThreadPoolExecutor() as executor:
      msg = json.loads(message.decode('utf-8'))
      executor.submit(handleCommand, msg)
      time.sleep(1)
  