#!/usr/bin/python
import socket
import sys
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = sys.argv[1]
port = int(sys.argv[2])

try:
    s.connect((addr, port))
except socket.gaierror, e:
    print "Address-related error connecting to server: %s" % e
    sys.exit(1)
except socket.error, e:
    print "Connection error: %s" % e
    sys.exit(1)


prompt="Client>> "
def Register(s):
	strng=s.recv(1024)
	print repr(strng)
	data = raw_input(prompt)
	if data=="2":
		s.send(data)
	
		strng=s.recv(1024)
		print repr(strng)
		Share(s)
	elif data=="3":
		s.send(data)
		strng=s.recv(1024)
		print repr(strng)
		Search(s)
	elif data=="Exit":
		s.send(data)


def Share(s):
	while True:
		data=raw_input(prompt)
		s.send(data)
		if data=="END":
			break	

def Search(s):
	#print "m in search"
	data = raw_input(prompt)
	s.send(data)
	i=0
	while True:
		#print "in loop " +str(i)
		#time.sleep(2)
		strng=s.recv(1024)
		if not strng:
			break
		if strng!="END" and strng!="NRF":
			print repr(strng)
		s.send("Done")
		if strng=="NRF":
			print prompt+"No Results Found"
			break
		if strng=="END":
			break
		i=i+1

while 1:
	string=s.recv(1024)
	print repr(string)
	data = raw_input(prompt)
	if data == "1":
		s.send(data)
		Register(s)
	elif data=="2":
		#print "client sharing"
		s.send(data)
		strng = s.recv(1024)
		print repr(strng)
		Share(s)
	elif data=="3":
		s.send(data)
		#print "client search"
		strng = s.recv(1024) #filename prompt
		print repr(strng)
		Search(s)
	elif data=="Exit":
		s.send(data)
		break
print "Connection Closed"
s.close()
