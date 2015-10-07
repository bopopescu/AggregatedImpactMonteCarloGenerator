import os
import csv
from numpy import loadtxt, concatenate



ups=os.listdir(os.path.join("correlated_impacts"))
for upName in ups:
	up=upName.strip("~")[:-4]
	try:
		up=int(up)
	except:
		ups.pop(ups.index(up+".csv"))
	ancien=loadtxt(os.path.join("correlated_impacts",str(up)+".csv"), delimiter=",", dtype=str)
	ancien2=loadtxt(os.path.join("correlated_impacts_bis",str(up)+".csv"), delimiter=",", dtype=str)
	nouveau = csv.writer(open(os.path.join("correlated_impacts",str(up)+".csv"), "wb"))
	for line in concatenate((ancien,ancien2)):
		newline=[]
		for number in line:
			try:
				number=float(number)
				newline.append(number)
			except:
				1
		if len(newline)==len(line):
			nouveau.writerow(newline)
