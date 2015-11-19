import socket
import cPickle as pickle
import threading
import pprint

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
NUM_SERVERS = 2
ports = [9997, 9996]
ips = ['10.0.2.61', '10.0.2.61']
lock = threading.Lock()
# count = 0

def print_mat():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	for i in range(n):
		for j in range(n):
			print G[i][j],
		print ''

def print_list(G):
	for i in G:
		print i
	# print ''

def cmp():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	x = 1
	for i in range(n):
		if opg[i] - npg[i] > 0.001:
			x = 0
	return x

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

def threadin(threadName, start, end, i):
	global G, edge_num, weights, it, d, pg, ih, oh, n, opg, npg, ports, count
	# print threadName
	# create a socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# get local machine name
	host = ips[i]
	port = ports[i]
	# connection to hostname on the port.
	s.connect((host, port))
	# print "bana kya?"

	dic = {'flag':0, 'opg':opg, 'start':start, 'end':end}
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(dic)
	st = pickle.dumps(dic,-1)
	s.send(st)

	npgs = s.recv(1024)
	s.close()
	npg_new = pickle.loads(npgs)

	lock.acquire()
	# count+=1
	# print count, "lock acquired by ", threadName, start, end
	# print "recieved", npg_new
	# print "old", npg

	for i in range(start,end+1):
		npg[i] = npg_new[i]
	# print "new", npg
	# print "lock released by ", threadName
	lock.release()

def pagerank():
	global G, edge_num, weights, it, d, pg, ih, oh, opg, npg, n
	count_oh()
	count_ih()
	# print oh
	# print ih
	opg = [(1.0/n) for x in range(n)]
	# print opg
	npg = [(0.0) for x in range(n)]

	dic = {'flag':1, 'graph':G,'n':n, 'd':d}
	for i in range(NUM_SERVERS):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# get local machine name
		host = ips[i]
		port = ports[i]
		# connection to hostname on the port.
		s.connect((host, port))
		
		st = pickle.dumps(dic,-1)
		s.send(st)

		s.close()

	while 1:
		# print "starting again"
		start =0
		end = n/NUM_SERVERS
		diff = end
		threads = []
		# print opg
		for i in range(NUM_SERVERS):
			# print "threading"
			t = threading.Thread( target=threadin, args=("Thread-" + str(i), start, end, i,) )
			threads.append(t)
			start = end+1
			end = min(n-1, end+diff)
			if i == NUM_SERVERS-2:
				end = n-1
			t.start()

		for t in threads:
			t.join()
			# print "hahahahhaha", t.result

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

	# print_mat()
	for i in range(edge_num):
		n1 = raw_input()
		G[ int(n1.split(' ')[0]) ][ int(n1.split(' ')[1]) ] = 1

	# print_mat()
	pagerank()
	print_list(opg)






if __name__ == '__main__':
	main()





