def transformation_matrices(A,B,uncert, UP_list, CF):
	from scipy.sparse import block_diag,hstack, lil_matrix, identity, csc_matrix, csr_matrix
	
	techno = lil_matrix(block_diag((A,[[1,0,0],[-0.1,1,0],[-0.2,-0.3,1]],[[1]])))
	interv = lil_matrix(hstack((B,[[1.1,1.2,1.3,1.4]]*len(B.todense()))))
	
	lA=len(A.todense())
	
	for i in range(3):
		uncert["technology"][lA+i]={lA+i:{"spread1":"NA","distribution":"NA","spread3":"NA","spread2":"NA"}}		
		for j in range(i):
			uncert["technology"][lA+i][lA+j]={"spread1":"NA","distribution":"Undefined","spread3":"NA","spread2":"NA"}
	uncert["technology"][lA+3]={lA+3:{"spread1":1.2,"distribution":"Lognormal","spread3":"0","spread2":"0"}}
	for i in range(4):
			UP_list+=["processus_test_"+str(i)]
			uncert["intervention"][lA-1+i]={0:{"spread1":"NA","distribution":"Undefined","spread3":"NA","spread2":"NA"}}
	
	CF_transformed=hstack((CF,identity(CF.shape[0])))
	
	return techno,interv,uncert, UP_list, CF_transformed
