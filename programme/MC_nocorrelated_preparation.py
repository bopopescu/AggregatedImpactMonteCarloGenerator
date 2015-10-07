def MC_nocorrelated_preparation(A, B, A_uncert, B_uncert, UP_list, UP_list_desag, mu, sign_ag, sigma):
	from numpy import log, sqrt, array, sign, exp
	import os
	import warnings
	
	warnings.simplefilter("ignore", RuntimeWarning)	
	
	nEF=B.shape[0]
	nUP=len(UP_list_desag)
	
	#lognormal=[x,y,sign,mu,sigma]
	#normal=[x,y,mu,sigma]
	#triangle=[x,y,min,max,mode]
	#deterministe=[x,y,valeur]
	lognormalA=[]
	normalA=[]
	triangleA=[]
	deterministeA=[]
	lognormalB=[]
	normalB=[]
	triangleB=[]
	deterministeB=[]
	agregeB=[]

	for column in range(nUP):
		c=UP_list.index(UP_list_desag[column]['process'])
		deterministeA.append((column,column,A[c, c]))
		for line in UP_list_desag[column]['enfants']:
			l=UP_list.index(UP_list_desag[line]['process'])
			if A_uncert[c][l]['distribution']=='Lognormal' and A_uncert[c][l]['spread1']>1 :
				lognormalA.append((line,column,A[l,c],log(abs(A[l, c])),log(sqrt(A_uncert[c][l]['spread1']))))			
			elif A_uncert[c][l]['distribution']=='Normal':
				normalA.append((line,column,A[l, c],A_uncert[c][l]['spread1']/2))
			elif A_uncert[c][l]['distribution']=='Triangle':
				triangleA.append((line,column,A[l, c],A_uncert[c][l]['spread2'],A_uncert[c][l]['spread3']))
			elif A_uncert[c][l]['distribution']=='Undefined':
				deterministeA.append([line,column,A[l, c]])
			elif A_uncert[c][l]['distribution']=='NA' and A[l, c]==1:
				deterministeA.append((line,column,A[l, c]))
			elif A_uncert[c][l]['distribution']=='Lognormal' and (A_uncert[c][l]['spread1']==1 or A[l, c]==0):
				deterministeA.append((line,column,A[l, c]))
			else:
				print A[l,c],A_uncert[c][l]
				raw_input()
		
		if UP_list_desag[column]['pruned']==1:#aggregated process
			for line in range(sigma.shape[0]):
				if sigma[line,c]!=0:
					agregeB.append((nEF+line, column, sign_ag[line,c], mu[line,c],sigma[line,c]))
				elif mu[line,c]!="-inf":
					deterministeB.append((nEF+line,column,sign_ag[line,c]*exp(mu[line,c])))
				else:
					print mu[line,c]
		
		else:#non aggregated process
			for line in B_uncert[c]:
				if B_uncert[c][line]['distribution']=='Lognormal' and B_uncert[c][line]['spread1']>1:
					lognormalB.append((line,column,B[line,c],log(abs(B[line, c])),log(sqrt(B_uncert[c][line]['spread1']))))
				elif B_uncert[c][line]['distribution']=='Normal':
					normalB.append((line,column,B[line, c],B_uncert[c][line]['spread1']/2))
				elif B_uncert[c][line]['distribution']=='Triangle':
					triangleB.append((line,column,B[line, c],B_uncert[c][line]['spread2'],B_uncert[c][line]['spread3']))
				elif B_uncert[c][line]['distribution']=='Undefined':
					deterministeB.append((line,column,B[line, c]))
				elif B_uncert[c][line]['distribution']=='Lognormal' and (B_uncert[c][line]['spread1']==1 or B[line, c]==0):
					deterministeB.append((line,column,B[line, c]))
				else:
					print B[line,c],B_uncert[c][line]
					raw_input()
	
	variables_technologique={"lognormal":array(lognormalA, object),"normal":array(normalA, object),"triangle":array(triangleA, object), "deterministe":array(deterministeA, object)}
	variables_intervention={"lognormal":array(lognormalB, object),"normal":array(normalB, object),"triangle":array(triangleB, object), "deterministe":array(deterministeB, object), "agregated":array(agregeB, object)}
	
	return variables_technologique, variables_intervention
		
