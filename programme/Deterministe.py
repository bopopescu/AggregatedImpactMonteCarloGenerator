def Deterministe(CF, UP_list, UP_list_desag, EF_list, technology_matrix, intervention_matrix, intensity_matrix, f,systems, system_number):
	from scipy.sparse import lil_matrix
	from print_mat_csv import print_mat
	from numpy import array,transpose,float32
	from numpy.linalg import solve
	import csv

	impact=array(transpose(CF.dot(intensity_matrix.dot(f))))
	print impact[0]
	
	#nEF=len(EF_list)
	#nUP=len(UP_list_desag)
	#fD=array([[0.0]]*nUP)
	
	#A = lil_matrix((nUP,nUP))
	#B = lil_matrix((nEF,nUP))
	
	#for column in range(nUP):
		#c=UP_list.index(UP_list_desag[column]['process'])
		#if UP_list_desag[column]['parent']=='RF':
			#fD[column,0]=f[UP_list_desag[column]['origine'],0]
		#A[column,column]=1.0
		#for line in range(nUP):
			#l=UP_list.index(UP_list_desag[line]['process'])
			#if line in UP_list_desag[column]['enfants']:
				#if technology_matrix[l,c]!=0:
					#A[line,column]=technology_matrix[l,c]
		#for line in range(nEF):
			#if UP_list_desag[column]['enfants']==[]:
				#if intensity_matrix[line,c]!=0:
					#B[line,column]=intensity_matrix[line,c]
			#elif intervention_matrix[line,c]!=0:
				#B[line,column]=intervention_matrix[line,c]

	#sD=solve(array(A.todense()),fD)
	#impactD=CF.dot(array(B.todense()).dot(sD))
	
	for UP in systems[system_number]:    
		name=UP_list.index(UP)
		c = csv.writer(open(str(name)+"D.csv", "wb"))

		c.writerow([UP])
		c.writerow(impact[0])
