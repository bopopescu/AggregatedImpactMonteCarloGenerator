def print_matrices_informations(uncertainties, CF):
	from scipy.sparse import find
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
	
	for matrix in lows:
		print "  "+matrix+" matrix"
		for low in lows[matrix]:
			print "     "+low+" : "+str(lows[matrix][low])
	print "  CF : "+str(nbr_elem_CF)+" (non 0 element)"
    
