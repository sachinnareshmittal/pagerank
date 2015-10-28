from random import randint

s = set()

n = int(raw_input("Number of nodes: "))
e = int(raw_input("Number of edges: "))
it = raw_input("Number of iterations: ")
df = raw_input("damping factor: ")

while len(s)!=e:
	n1 = randint(0,n-1);
	n2 = randint(0,n-1);
	if n1 == n2:
		continue
	st = str(n1)+" "+str(n2)
	s.add(st)

f = open("input","w")
f.write(str(n)+"\n"+str(e)+"\n"+str(it)+"\n"+str(df)+"\n")

for l in s:
	f.write(l+"\n")

f.close()