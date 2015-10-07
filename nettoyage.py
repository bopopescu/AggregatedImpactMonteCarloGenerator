import os
import csv
from numpy import loadtxt, concatenate, genfromtxt


ncol=5
ups=os.listdir(os.path.join("correlated_impacts"))
for upName in ups:
	up=upName.strip("~")[:-4]
	try:
		up=int(up)
	except:
		ups.pop(ups.index(up+".csv"))
	
	ancien=genfromtxt(os.path.join("correlated_impacts",str(up)+".csv"), delimiter=",", dtype=str,invalid_raise=False, skip_header=10)
	try:
		ancien2=genfromtxt(os.path.join("correlated_impacts_bis",str(up)+".csv"), delimiter=",", dtype=str,invalid_raise=False )
		ancien=concatenate((ancien,ancien2))
	except:
		1
	nouveau = csv.writer(open(os.path.join("correlated_impacts",str(up)+".csv"), "wb"))
	for line in ancien:
		newline=[]
		for number in line:
			try:
				number=float(number)
				newline.append(number)
			except:
				1
		if len(newline)==ncol:
			nouveau.writerow(newline)
