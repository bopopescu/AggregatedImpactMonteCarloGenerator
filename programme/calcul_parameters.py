def calcul_parameters(UP_list, path, nb_categories):
	from numpy import loadtxt, log, sqrt, var, mean, transpose, matrix, abs, sign
	import os
	
	sigma=[]
	mu=[]
	sgn=[]
	
	up_calc=os.listdir(path)
	for up in range(len(UP_list)):
		if str(up)+".csv" in up_calc:
			try:
				data=loadtxt(open(os.path.join(path,str(up)+".csv"), "rb"), delimiter=",", dtype=float)
			except:
				print up
				raw_input()
			variance=var(data,0)
			E=mean(data,0)
			line_sigma=[]
			line_mu=[]
			line_sgn=[]
			for (v,e) in zip(variance,E):
				if e==0 or v==0:
					line_sigma.append(0)
					line_mu.append(0)
					line_sgn.append(0)
				else:
					s2=log(1+v/(e*e))
					line_sigma.append(sqrt(s2))
					line_mu.append(log(abs(e))-s2/2)
					line_sgn.append(sign(e))
			sigma.append(line_sigma)
			mu.append(line_mu)
			sgn.append(line_sgn)
		else:
			sigma.append(['-']*nb_categories)
			mu.append(['-']*nb_categories)
			sgn.append(['-']*nb_categories)

	return transpose(matrix(sigma)), transpose(matrix(mu)), transpose(matrix(sgn))
