def print_mat_desag(MATA, MATB,incertitude, UP_list_desag,EF_list):
	from openpyxl.workbook import Workbook
	from openpyxl.worksheet import Worksheet
	from copy import copy
	from time import time
	from scipy.sparse import lil_matrix, find

	filename = 'MAT.xlsx'
	wb = Workbook(encoding = 'mac_roman')
	Ws=wb.active
	wb.remove_sheet(Ws)
	
	
	#creation de la matrice A avec sa matrice d'incertitude
	Ws = Worksheet(wb, title = 'Processus')  
	for UP in UP_list_desag:
		line=[UP,UP_list_desag[UP]['origine']]
		line.append(UP_list_desag[UP]['process'])
		line.append(str(UP_list_desag[UP]['enfants']))
		Ws.append(line)	
	wb.add_sheet(Ws)
	
	Ws = Worksheet(wb, title = 'A')  
	Ws.freeze_panes = 'B2'
	mat=MATA.toarray()
	header = ['A']
	for UP in UP_list_desag:
		header.append(UP_list_desag[UP]['process'])
	Ws.append(header)
	for row in range(len(mat)):
		line=[row]
		for col in range(len(mat[row])):
			line.append(mat[row][col])
		Ws.append(line)	
	wb.add_sheet(Ws)
	
	Ws = Worksheet(wb, title = 'incertitude A')
	Ws.freeze_panes = 'B2'
	mat=incertitude['technology']
	header = ['incertitude A']
	for UP in UP_list_desag:
		header.append(UP_list_desag[UP]['process'])
	Ws.append(header)
	for row in range(len(mat)):
		line=[row]
		for col in range(len(mat)):
			line.append(mat[col][row])
		Ws.append(line)	
	wb.add_sheet(Ws)
	
	
	#Creation de B avec sa matrice d'incertitude
	Ws = Worksheet(wb, title = 'Flux elem') 
	Ws.freeze_panes = 'A2'
	header = ['id','compartment', 
          'substance', 
          'subcompartment']
	Ws.append(header)
	for EF in EF_list:
		L=[EF_list.index(EF)]
		L.append(EF)
		Ws.append(L)
	wb.add_sheet(Ws)
    
	Ws = Worksheet(wb, title = 'B')
	Ws.freeze_panes = 'B2'
	mat=MATB.toarray()
	header = ['B']
	for UP in UP_list_desag:
		header.append(UP_list_desag[UP]['process'])
	Ws.append(header)
	for row in range(len(mat)):
		line=[row]
		for col in range(len(mat[row])):
			line.append(mat[row][col])
		Ws.append(line)	
	wb.add_sheet(Ws)

	Ws = Worksheet(wb, title = 'incertitude B')
	Ws.freeze_panes = 'B2'
	mat=incertitude['intervention']
	header = ['incertitude B']
	for UP in UP_list_desag:
		header.append(UP_list_desag[UP]['process'])
	Ws.append(header)
	for row in range(len(mat[0])):
		line=[row]
		for col in range(len(mat)):
			line.append(mat[col][row])
		Ws.append(line)	
	wb.add_sheet(Ws)
	
	
	
	wb.save(filename)
	
	print 'fichier enregistre : MAT.xlsx'
