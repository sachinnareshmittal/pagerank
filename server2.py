import socket
import time
import cPickle as pickle
import pprint
import struct

n = 1
edge_num = 0
weights = []
G = []
it = 0
d = 1
pg = []
ih = []
oh = []
opg = []
npg = []
host = "10.0.2.61"
port = 9996


def send_msg(sock, msg):
	msg = struct.pack('>I', len(msg)) + msg
	sock.sendall(msg)

def recv_msg(sock):
	raw_msglen = recvall(sock, 4)
	if not raw_msglen:
		return None
	msglen = struct.unpack('>I', raw_msglen)[0]
	return recvall(sock, msglen)

def recvall(sock, n):
	data = ''
	while len(data) < n:
		packet = sock.recv(n - len(data))
		if not packet:
			return None
		data += packet
	return data

def count_oh():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	for i in range(n):
		n_out = 0
		for j in range(n):
			# print i,j
			if G[i][j]==1:
				n_out+=1
		oh.append(n_out)

def count_ih():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	for i in range(n):
		n_in = 0
		for j in range(n):
			if G[j][i]==1 :
				n_in+=1
		ih.append(n_in)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serversocket.bind((host, port))

serversocket.listen(1000)

while True:
	clientsocket,addr = serversocket.accept()
	print("Got a connection from %s" % str(addr))
	
	s = recv_msg(clientsocket)
	print "recieved!!"
	dic = pickle.loads(s)

	if dic['flag'] == 1:
		G = dic['graph']
		n = dic['n']
		d = dic['d']
		count_ih()
		count_oh()
	else:
		opg = dic['opg']
		start = dic['start']
		end = dic['end']
		npg = [0.0 for x in range(n)]
		dp = 0.0
		for p in range(n):
			if oh[p] == 0:
				dp += float(d*opg[p]/n)

		for p in range(start,end+1):
			npg[p] = float(dp + (1.0-d)/n)

			for ip in range(n):
				if G[ip][p] == 1:
					npg[p] += float(d*float(opg[ip])/float(oh[ip]))

		x = pickle.dumps(npg,-1)
		send_msg(clientsocket,x)
		print "sent!!"
	clientsocket.close()