from numpy import loadtxt, mean



data=loadtxt(open("Climate_change.csv", "rb"), delimiter=",", dtype=float)

E=mean(data,1)

for process in range(len(E)):
	for iteration in range(len(data[process,:])):
		if data[process,iteration]>5*E[process] or data[process,iteration]<0.2*E[process]:
			print "process : "+str(process),
			print ", iteration : "+str(iteration),
			print ", moyenne : "+str(E[process]),
			print ", valeur : "+str(data[process,iteration]),
			raw_input()

