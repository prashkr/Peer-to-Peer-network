#p2p network using socket programming.

#!/usr/bin/python
import socket
from threading import Thread
import os
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",2500))
s.listen(10)
greetings = ["1.Register", "2.Share FIles", "3.Search File"]
peer_list = []
file_list = {}
addr_list = {}
prompt = "Server>>"

def delete(socket, addr):
	print "address list dictionary"
	for key in addr_list:
		print key, addr_list[key]
	print ""
	print "printing peer list"
	for i in peer_list:
		print i
	print ""

	print "printint file list dictionary"
	for key in file_list:
		print key, file_list[key]
	print ""

	print "deleting address " + addr
	tempList=[]
	for key in addr_list:
		if key==addr:
			tempList.append(key)
	for i in tempList:
		del addr_list[i]
	
	if peer_list.count(addr)>0:
		index = peer_list.index(addr)
		del peer_list[index]
	for key in file_list:
		list = file_list[key]
		print "list for key "+ key
		for i in list:
			print i
		index_list=[]
		for i in list:
			
			temp = i.split(" ")			
			if temp[0]==addr:
				print "address matched"
				index_list.append(list.index(i))
		print "printing index list"
		for i in index_list:
			print i

		for i in index_list:
			del file_list[key][i]

	print "address list dictionary"
	for key in addr_list:
		print key, addr_list[key]
	print ""
	print "printing peer list"
	for i in peer_list:
		print i
	print ""

	print "printing file list dictionary"
	for key in file_list:
		print key, file_list[key]
	print ""


def Register(sockets,addr):
	peer_list.append(addr)
	print addr+" is now registered"
	sockets.sendall(prompt+"Registration Done! Press 2 for file sharing or 3 for searching: ")
	temp=sockets.recv(1024)
	if temp=="2":
		Share(sockets,addr)	
	elif temp=="3":
		Search(sockets)

def Share(sockets,addr):
	sockets.sendall(prompt+"Enter Filename as '<filename> <location>' and when you are done type 'END' to stop: ")
	strng=sockets.recv(1024)
	while True:
		filename, location = strng.split(" ")
		if file_list.has_key(filename):
			temp_list = file_list[filename]
			temp_list.append(addr + " " + location)
		else:
			temp_list = []
			temp_list.append(addr + " " + location)
		file_list.update({filename:temp_list})
		#print ""
		#print "printing file list"
		#for key in file_list:
		#	print key,file_list[key]

		if addr_list.has_key(addr):
			temp_list = addr_list[addr]
			if temp_list.count(filename)==0:
				temp_list.append(filename)
		else:
			temp_list = []
			temp_list.append(filename)
		addr_list.update({addr:temp_list})
		#print ""
		#print "printing addr list"
		#for key in addr_list:
		#	print key,addr_list[key]

		strng=sockets.recv(1024)
		if strng == "END":
			break

def Search(sockets):
	#print "server search begin"
	sockets.sendall(prompt+"Enter filename and when you are done type 'END': ")
	searchFor=sockets.recv(1024)
	if file_list.has_key(searchFor):
		temp_list = file_list[searchFor]
		#temp_list.append("END")
		#for i in file_list[searchFor]:
		#	print i
		for i in range(len(temp_list)):
			sockets.sendall(temp_list[i])
	#		print "result sent"
			status=sockets.recv(1024)
	#		print status
		sockets.sendall("END")
		sockets.recv(1024)
	else:
		sockets.sendall("NRF")
		sockets.recv(1024)

def clients():
	sockets, (addr, port) = s.accept()
	count=0
	print addr+" is Connected" 
	while True:
	#	print "server loop begin"
		if peer_list.count(addr)==0 :
			try:
				sockets.sendall(greetings[0] + " " + greetings[1]+" "+ greetings[2]+" or Type 'Exit' to drop connection: ")	
			except:
				pass
			string = sockets.recv(1024)
			if string == "1":
				Register(sockets,addr)	
			elif string=="2":
				continue
			elif string=="3":
				Search(sockets)
			elif string=="Exit":
				break
			count = count+1
		else:
			if count==0:
				sockets.sendall(prompt+"Hello "+ addr +" ::"+"Choose : " + greetings[1]+" "+ greetings[2]+" or Type 'Exit' to drop connection: ")
			else:
				sockets.sendall(prompt+"Choose : " + greetings[1]+" "+ greetings[2]+" or Type 'Exit' to drop connection: ")
			print 
			temp=sockets.recv(1024)
			#print "temp is "+temp
			if temp=="2":
				Share(sockets,addr)
			elif temp=="3":
				Search(sockets)
			elif temp=="Exit":
				break
			count = count+1
	#	print "server loop end"
	print addr+" Disconnected"
	delete(sockets, addr)
	sockets.close()
print "Waiting for peers"
for i in range(20):
	Thread(target=clients).start()
	
s.close()

