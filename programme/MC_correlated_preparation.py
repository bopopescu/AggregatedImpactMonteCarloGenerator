def MC_correlated_preparation(A, B, Aincert, Bincert):
	from numpy import log, sqrt, array, sign, exp
	import os
	import warnings
	
	warnings.simplefilter("ignore", RuntimeWarning)	
	
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
	
	for column in Aincert:
			for line in Aincert[column]:
				if Aincert[column][line]['distribution']=='Lognormal' and Aincert[column][line]['spread1']>1 :
					lognormalA.append((line,column,A[line,column],log(abs(A[line, column])),log(sqrt(Aincert[column][line]['spread1']))))			
				elif Aincert[column][line]['distribution']=='Normal' :
					normalA.append((line,column,A[line, column],Aincert[column][line]['spread1']/2))
				elif Aincert[column][line]['distribution']=='Triangle' :
					triangleA.append((line,column,A[line, column],Aincert[column][line]['spread2'],Aincert[column][line]['spread3']))
				elif Aincert[column][line]['distribution']=='Undefined' :
					deterministeA.append([line,column,A[line, column]])
				elif Aincert[column][line]['distribution']=='NA' and A[line, column]==1:
					deterministeA.append((line,column,A[line, column]))
				elif Aincert[column][line]['distribution']=='Lognormal' and Aincert[column][line]['spread1']==1:
					deterministeA.append((line,column,A[line, column]))
				else:
					print "colonne : "+ str(column)+", line : "+str(line)+", value : "+str(A[line,column])+", incertitude : "+str(Aincert[column][line])
					raw_input()
	
	for column in Bincert:
			for line in Bincert[column]:
				if Bincert[column][line]['distribution']=='Lognormal' and Bincert[column][line]['spread1']>1:
					lognormalB.append((line,column,B[line,column],log(abs(B[line, column])),log(sqrt(Bincert[column][line]['spread1']))))
				elif Bincert[column][line]['distribution']=='Normal' :
					normalB.append((line,column,B[line, column],Bincert[column][line]['spread1']/2))
				elif Bincert[column][line]['distribution']=='Triangle' :
					triangleB.append((line,column,B[line, column],Bincert[column][line]['spread2'],Bincert[column][line]['spread3']))
				elif Bincert[column][line]['distribution']=='Undefined' :
					deterministeB.append((line,column,B[line, column]))
				elif Bincert[column][line]['distribution']=='Lognormal' and Bincert[column][line]['spread1']==1:
					deterministeB.append((line,column,B[line, column]))
				else:
					print B[line,column],Bincert[column][line]
					raw_input()
	
	variables_technologique={"lognormal":array(lognormalA, object),"normal":array(normalA, object),"triangle":array(triangleA, object), "deterministe":array(deterministeA, object)}
	variables_intervention={"lognormal":array(lognormalB, object),"normal":array(normalB, object),"triangle":array(triangleB, object), "deterministe":array(deterministeB, object),"agregated":array([],object)}
	
	return variables_technologique, variables_intervention
		
