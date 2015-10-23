def calcul_vcv(UP_list, impact_method, CF_categories_name, path):
	from numpy import loadtxt,cov
	import csv
	import os
	
	for category in CF_categories_name:
		#print "\rcontruction of impacts matrix for "+category+"                    ",
		with open(os.path.join(path,"correlated_impacts",category+".csv"),"wb") as impacts_matrix:
			MAT=csv.writer(impacts_matrix)
			for up in range(len(UP_list)):
				try:
					data_up = loadtxt(os.path.join(path,"correlated_impacts",str(up)+".csv"),delimiter=",", usecols=(CF_categories_name.index(category),), dtype=float)
					MAT.writerow(data_up)
				except:
					print up
				

	for category in CF_categories_name:
		#print "\rconstructions of variance-covariance matrix for "+category+"                    ",
		data_vcv=loadtxt(os.path.join(path,"correlated_impacts",category+".csv"), delimiter=",", dtype=float)
		vcv=csv.writer(open(os.path.join(path,"variance_covariance",category+".csv"),"wb"))
		vcv_mat=cov(data_vcv,rowvar=1)
		
		for i in range(1,len(vcv_mat)):
			vcv.writerow(vcv_mat[i,:i])
	#print "\rvariance-covariance matrices constructed                              "
