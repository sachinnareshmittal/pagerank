import socket
import cPickle as pickle
import threading
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
NUM_SERVERS = 3
PRECISION = 0.0000000001
ports = [9997, 9996, 9995]
ips = ['10.0.2.61', '10.0.2.61', '10.0.2.61']
lock = threading.Lock()

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


def print_mat():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	for i in range(n):
		for j in range(n):
			print G[i][j],
		print ''

def print_list(G):
	for i in G:
		print i

def cmp():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	x = 1
	for i in range(n):
		if opg[i] - npg[i] > PRECISION:
			x = 0
	return x

def count_oh():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	for i in range(n):
		n_out = 0
		for j in range(n):
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

def threadin(threadName, start, end, i):
	global G, edge_num, weights, it, d, pg, ih, oh, n, opg, npg, ports, count

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	host = ips[i]
	port = ports[i]

	s.connect((host, port))

	dic = {'flag':0, 'opg':opg, 'start':start, 'end':end}
	st = pickle.dumps(dic,-1)
	send_msg(s,st)

	npgs = recv_msg(s)
	npg_new = pickle.loads(npgs)

	lock.acquire()
	for i in range(start,end+1):
		npg[i] = npg_new[i]
	lock.release()

def pagerank():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	count_oh()
	count_ih()
	opg = [(1.0/n) for x in range(n)]
	npg = [(0.0) for x in range(n)]

	dic = {'flag':1, 'graph':G,'n':n, 'd':d}
	print "sending graph"
	for i in range(NUM_SERVERS):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		host = ips[i]
		port = ports[i]
		s.connect((host, port))
		
		st = pickle.dumps(dic,-1)
		send_msg(s, st)

		s.close()
	
	print "graph sent"
	while 1:
		start =0
		end = n/NUM_SERVERS
		diff = end
		threads = []
		for i in range(NUM_SERVERS):
			t = threading.Thread( target=threadin, args=("Thread-" + str(i), start, end, i,) )
			threads.append(t)
			start = end+1
			end = min(n-1, end+diff)
			if i == NUM_SERVERS-2:
				end = n-1
			t.start()

		for t in threads:
			t.join()

		if cmp()==1:
			break

		opg = [x for x in npg]
		it+=1
	print "number of iterations = ", it



def main():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	n = int(raw_input())
	edge_num = int(raw_input())
	weights = [(1.0/n) for x in range(n)]
	G = [[0 for x in range(n)] for x in range(n)]
	
	it = int(raw_input())
	d = float(raw_input())

	for i in range(edge_num):
		n1 = raw_input()
		G[ int(n1.split(' ')[0]) ][ int(n1.split(' ')[1]) ] = 1

	pagerank()
	print_list(opg)

if __name__ == '__main__':
	main()