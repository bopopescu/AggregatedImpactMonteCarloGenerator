def construct_UP_list_desag(desag_retour,UP_list):
	L={}
	for UP in desag_retour:
		L[UP]={}
		L[UP]['parent']=desag_retour[UP]['parent']
		L[UP]['pruned']=desag_retour[UP]['pruned']
		L[UP]['demand']=desag_retour[UP]['demand']
		L[UP]['origine']=desag_retour[UP]['UP_number']
		L[UP]['process']=UP_list[desag_retour[UP]['UP_number']]
		L[UP]['enfants']=[]
		for UP_enf in desag_retour:
			if desag_retour[UP_enf]['parent']==UP:
				L[UP]['enfants'].append(UP_enf)
    
	return L
