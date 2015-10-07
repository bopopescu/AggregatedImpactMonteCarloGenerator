def build_mat_desag(UP_list, UP_list_desag, EF_list, A, B, mu_BAinv, sigma_BAinv, Aincert, Bincert,f):
	from scipy.sparse import lil_matrix
	from numpy import array, random, log, sqrt, float32, sign, exp
	
	nEF=len(EF_list)
	nUP=len(UP_list_desag)
	fD=array([[0.0]]*nUP)

	mu_A = lil_matrix((nUP,nUP))
	sigma_A= lil_matrix([[1.0]*nUP]*nUP)
	UA= lil_matrix((nUP,nUP))
	DA= lil_matrix((nUP,nUP))
	mu_B = lil_matrix((nEF,nUP))
	sigma_B = lil_matrix([[1.0]*nUP]*nEF)
	UB = lil_matrix((nEF,nUP))
	DB = lil_matrix((nEF,nUP))
	
	for column in range(nUP):
		
		print '\r col',column,'/',nUP
		c=UP_list.index(UP_list_desag[column]['process'])
		
		if f[UP_list_desag[column]['origine'],0]!=0:
			fD[column,0]=f[UP_list_desag[column]['origine'],0]
		
		for line in UP_list_desag[column]['enfants']:
			l=UP_list.index(UP_list_desag[line]['process'])
			
			if  Aincert[c][l]['distribution']=='Lognormal' and Aincert[c][l]['spread1']>1 and A[l,c]!=0:
				sgn=sign(A[l,c])
				sigma=float32(log(sqrt(Aincert[c][l]['spread1'])))
				mu=float32(log(abs(A[l,c])))
				UA[line,column]=sgn
				sigma_A[line,column] = sigma
				mu_A[line,column] = mu
			elif A[l,c]!='NA':
				DA[line,column] = float32(A[l,c])
		
		if UP_list_desag[column]['enfants']==[]:#processus agrege
			for line in range(nEF):
				if sigma_BAinv[line,c]!=0:
					sgn=sign(mu_BAinv[line,c])
					sigma=sigma_BAinv[line,c]
					mu=abs(mu_BAinv[line,c])
					UB[line,column]=sgn
					sigma_B[line,column] = sigma
					mu_B[line,column] = mu
					if sigma=="nan" or mu=="nan":
						print sigma, mu
				else:
					DB[line,column]=float32(mu_BAinv[line,c])
					
		else:
			for line in Bincert[c]:#processus desagrege avec incertitude
				if Bincert[c][line]['distribution']=='Lognormal' and Bincert[c][line]['spread1']>1 and B[line,c]!=0:
					sgn=sign(B[line,c])
					mu=float32(log(abs(B[line,c])))
					sigma=float32(log(sqrt(Bincert[c][line]['spread1'])))
					UB[line,column]=sgn
					sigma_B[line,column] = sigma
					mu_B[line,column] = mu
				else:
					DB[line,column] = float32(B[line,c])
	

	return array(mu_A.todense(),float32),array(mu_B.todense(),float32), array(sigma_A.todense(),float32),array(sigma_B.todense(),float32), array(UA.todense(),float32),array(UB.todense(),float32),array(DA.todense(),float32),array(DB.todense(),float32),fD
