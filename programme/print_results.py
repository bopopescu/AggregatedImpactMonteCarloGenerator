def print_results(path, project_name, UP_list, EF_list, impact_method, CF_categories, CF_units, iterations, disaggregation_criterion, uncertainties, CF):
	import csv
	from scipy.sparse import find
	import os
	
	
	info = csv.writer(open(os.path.join(path,"info.csv"),"wb"))
	
	info.writerows([["Project name : "+project_name],["Monte-Carlo iterations : "+str(iterations)],["disagregation criterion : "+str(disaggregation_criterion*100)+"%"],["Impact methode : "+impact_method],["Categories"],[category+" ("+unit+")" for category,unit in zip(CF_categories,CF_units)],[]])
	
	lows={}
	for matrice in uncertainties:
		lows[matrice]={}
		for up1 in uncertainties[matrice]:
			for up2 in uncertainties[matrice][up1]:
				try:
					lows[matrice][uncertainties[matrice][up1][up2]["distribution"]]+=1
				except:
					lows[matrice][uncertainties[matrice][up1][up2]["distribution"]]=1
	nbr_elem_CF=len(find(CF)[0])
	
	print "Summary : "
	info.writerow(["Database Summary"])
	print "   Technology matrix"
	info.writerow(["Technology matrix"])
	print "      Total amount of parameters in the matrix : "+str(len(UP_list)*len(UP_list))
	info.writerow(["elements",len(UP_list)*len(UP_list)])
	print "      Number of non-zero elements : "+str(sum([lows["technology"][low] for low in lows["technology"]]))+" (sparcity = "+str(round(float(sum([lows["technology"][low] for low in lows["technology"]]))/float(len(UP_list)*len(UP_list))*100,2))+"%)"
	info.writerow(["non zero elements",sum([lows["technology"][low] for low in lows["technology"]])])
	try:
		print "      Number of parameters with no associated uncertainty information : "+str(lows["technology"]["NA"]+lows["technology"]["Undefined"])+" ("+str(round(float(lows["technology"]["NA"]+lows["technology"]["Undefined"])/float(sum([lows["technology"][low] for low in lows["technology"]]))*100))+"%)"
		info.writerow(["Undefinied distribution", lows["technology"]["NA"]+lows["technology"]["Undefined"]])
	except:
		1
	try:
		print "      Number of parameters with lognormal distribution : "+str(lows["technology"]["Lognormal"])+" ("+str(round(float(lows["technology"]["Lognormal"])/float(sum([lows["technology"][low] for low in lows["technology"]]))*100,2))+"%)"
		info.writerow(["Lognormal distribution", lows["technology"]["Lognormal"]])
	except:
		1
	try:
		print "      Number of parameters with normal distribution : "+str(lows["technology"]["Normal"])+" ("+str(round(float(lows["technology"]["Normal"])/float(sum([lows["technology"][low] for low in lows["technology"]]))*100,2))+"%)"
		info.writerow(["Normal distribution", lows["technology"]["Normal"]])
	except:
		1
	try:
		print "      Number of parameters with triangular distribution : "+str(lows["technology"]["Triangle"])+" ("+str(round(float(lows["technology"]["Triangle"])/float(sum([lows["technology"][low] for low in lows["technology"]]))*100,2))+"%)"
		info.writerow(["Triangular distribution", lows["technology"]["Triangle"]])
	except:
		1
	
	
	print "   Intervention matrix"
	info.writerows([[],["Intervention matrix"]])
	print "      Total amount of parameters in the matrix : "+str(len(UP_list)*len(EF_list))
	info.writerow(["elements",len(UP_list)*len(EF_list)])
	print "      Number of non-zero elements : "+str(sum([lows["intervention"][low] for low in lows["intervention"]]))+" (sparcity = "+str(round(float(sum([lows["intervention"][low] for low in lows["intervention"]]))/float(len(UP_list)*len(EF_list))*100,2))+"%)"
	info.writerow(["non zero elements",sum([lows["intervention"][low] for low in lows["intervention"]])])
	try:
		print "      Number of parameters with no associated uncertainty information : "+str(lows["intervention"]["Unspecified"])+" ("+str(round(float(lows["intervention"]["Unspecified"])/float(sum([lows["intervention"][low] for low in lows["intervention"]]))*100,2))+"%)"
		info.writerow(["Undefinied distribution", lows["intervention"]["Unspecified"]])
	except:
		1
	try:
		print "      Number of parameters with lognormal distribution : "+str(lows["intervention"]["Lognormal"])+" ("+str(round(float(lows["intervention"]["Lognormal"])/float(sum([lows["intervention"][low] for low in lows["intervention"]]))*100,2))+"%)"
		info.writerow(["Lorgnormal distribution", lows["intervention"]["Lognormal"]])
	except:
		1
	try:
		print "      Number of parameters with normal distribution : "+str(lows["intervention"]["Normal"])+" ("+str(round(float(lows["intervention"]["Normal"])/float(sum([lows["intervention"][low] for low in lows["intervention"]]))*100,2))+"%)"
		info.writerow(["Normal distribution", lows["intervention"]["Normal"]])
	except:
		1
	try:
		print "      Number of parameters with triangular distribution : "+str(lows["intervention"]["Triangle"])+" ("+str(round(float(lows["intervention"]["Triangle"])/float(sum([lows["intervention"][low] for low in lows["intervention"]]))*100,2))+"%)"
		info.writerow(["Triangular distribution", lows["intervention"]["Triangle"]])
	except:
		1

	print "   Caracterization factors matrix"
	info.writerows([[],["Caracterization factors matrix"]])
	print "      Total amount of parameters in the matrix : "+str(len(UP_list)*len(EF_list))
	info.writerow(["elements", len(UP_list)*len(EF_list)])
	print "      Number of non-zero elements : "+str(nbr_elem_CF)+" (sparcity = "+str(round(float(nbr_elem_CF)/float(len(UP_list)*len(EF_list))*100,2))+"%)"
	info.writerow(["non zero elements", nbr_elem_CF])
			
	info.writerows([[],["Processus"], range(len(UP_list)), [up for up in UP_list],[],["Elementary flow"], range(len(EF_list)), [' | '.join(ef) for ef in EF_list], [ef[1] for ef in EF_list], [ef[0] for ef in EF_list], [ef[2] for ef in EF_list]])
	
	info.writerows([[],["Files constructions"]])
	info.writerow(["folder","files name","columns", "rows", "description"])
	info.writerow(["correlated_impacts","index processus", "Impact category", "iterations", "result of the Monte-Carlo simulation in the correlated case (by processus)"])
	info.writerow(["correlated_impacts","Impact category", "iterations", "index processus", "result of the Monte-Carlo simulation in the correlated case (by category)"])
	info.writerow(["nocorrelated_impacts","index processus", "Impact category", "iterations", "result of the Monte-Carlo simulation in the non correlated case (by processus)"])
	info.writerow(["variance_covariance","impact category", "index processus", "index processus +1", "mariance-covariance matrix (by category), without diagonal"])
	info.writerow(["Trees", "index processus", "-", "-", "Tree corresponding to the life cycle for the disagregation criterion (by processus)"])	
