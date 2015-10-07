def MC(variables_techno, variables_interv, CF, CF_categories_name, iterations, UP_list, system_number, path, systems, progress):
	from numpy import log, random, sqrt, array, sign, exp, transpose, float32, max, matrix
	from numpy.linalg import solve
	from scipy.sparse import lil_matrix, identity
	from fix_inverse import fix_inverse
	from scipy.linalg import inv
	from time import time,sleep
	import os
	import csv
	from Tkinter import Tk, IntVar
	import ttk
	import threading
	
	def matrices(UP_list,CF, variables_techno, variables_interv):
			
		MA=lil_matrix((len(UP_list),len(UP_list)))
		MB=lil_matrix((CF.shape[1],len(UP_list)))
		
		if len(variables_techno["lognormal"])>0:
			MA[array(variables_techno["lognormal"][:,0],int),array(variables_techno["lognormal"][:,1],int)] =sign(variables_techno["lognormal"][:,2])*random.lognormal(array(variables_techno["lognormal"][:,3],float32),array(variables_techno["lognormal"][:,4],float32))
		if len(variables_techno["normal"])>0:
			MA[array(variables_techno["normal"][:,0],int),array(variables_techno["normal"][:,1],int)] = random.normal(array(variables_techno["normal"][:,2],float32),array(variables_techno["normal"][:,3],float32))
		if len(variables_techno["triangle"])>0:
			MA[array(variables_techno["triangle"][:,0],int),array(variables_techno["triangle"][:,1],int)] = sign(variables_techno["triangle"][:,2])*random.triangular(array(variables_techno["triangle"][:,3],float32),abs(array(variables_techno["triangle"][:,2],float32)),array(variables_techno["triangle"][:,4],float32))
		if len(variables_techno["deterministe"])>0:
			MA[array(variables_techno["deterministe"][:,0],int),array(variables_techno["deterministe"][:,1],int)] = variables_techno["deterministe"][:,2]
		
		if len(variables_interv["lognormal"])>0:
			MB[array(variables_interv["lognormal"][:,0],int),array(variables_interv["lognormal"][:,1],int)] =sign(variables_interv["lognormal"][:,2])*random.lognormal(array(variables_interv["lognormal"][:,3],float32),array(variables_interv["lognormal"][:,4],float32))
		if len(variables_interv["normal"])>0:
			MB[array(variables_interv["normal"][:,0],int),array(variables_interv["normal"][:,1],int)] = random.normal(array(variables_interv["normal"][:,2],float32),array(variables_interv["normal"][:,3],float32))
		if len(variables_interv["triangle"])>0:
			MB[array(variables_interv["triangle"][:,0],int),array(variables_interv["triangle"][:,1],int)] = sign(variables_interv["triangle"][:,2])*random.triangular(array(variables_interv["triangle"][:,3],float32),abs(array(variables_interv["triangle"][:,2],float32)),array(variables_interv["triangle"][:,4],float32))
		if len(variables_interv["agregated"])>0:
			MB[array(variables_interv["agregated"][:,0],int),array(variables_interv["agregated"][:,1],int)] = variables_interv["agregated"][:,2]*random.lognormal(array(variables_interv["agregated"][:,3],float32),array(variables_interv["agregated"][:,4],float32))
		if len(variables_interv["deterministe"])>0:
			MB[array(variables_interv["deterministe"][:,0],int),array(variables_interv["deterministe"][:,1],int)] = variables_interv["deterministe"][:,2]
		
		return MA, MB
		
	if system_number=="all":
		f=identity(len(UP_list))
	else:
		f=lil_matrix((len(UP_list),1))
		f[0,0]=1
	
	
	for k in range(iterations):
		
		progress.set((k+1)*100/iterations)

		MA,MB=matrices(UP_list,CF, variables_techno, variables_interv)
		
		if system_number=="all":
			
			MAinv=inv(MA.todense())
			Z = (identity(len(MA.todense())) - MA)
			MAinv = fix_inverse(Z, MAinv)
			
			impact=CF * MB * MAinv * f
			
			for sys in range(impact.shape[1]):
				with open(os.path.join(path,str(sys)+".csv"), "ab") as fichier:
					csv_results = csv.writer(fichier)
					csv_results.writerow(impact[:,sys])
			#print '\r   Progress of Monte-Carlo simulations : '+str(int(100*(k+1)/iterations))+"%  ",
		
		else:
			
			s=solve(MA.todense(),f.todense())
			impact=array(CF*MB*s)[:,0]
			
			with open(os.path.join(path,str(system_number)+".csv"), "ab") as fichier:
					csv_results = csv.writer(fichier)
					csv_results.writerow(impact)
			#print "\r  system : "+str(system_number)+"/"+str(len(systems)-5)+", Progress of Monte-Carlo simulations : "+str(int(100*(k+1)/iterations))+"%      ",
