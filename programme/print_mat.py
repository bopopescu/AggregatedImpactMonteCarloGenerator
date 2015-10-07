def print_mat(MAT,nom):
	from openpyxl.workbook import Workbook
	from openpyxl.worksheet import Worksheet
	from numpy import array
	import csv
	import os
	
	wb = Workbook(encoding = 'mac_roman') #creating a workbook
	ws = Worksheet(wb, title = nom) #creating a sheet inside the workbook
    
	mat=MAT
	for row in range(len(mat)):
		ws.append(mat[row].tolist());

	wb.add_sheet(ws)
	wb.save(nom+'.xlsx')
    	
	os.startfile(nom+".xlsx")
	
	
def print_mat_csv(MAT,nom):
	import csv
	import os
	c = csv.writer(open(nom+".csv", "wb"))
	mat=MAT
	for row in range(len(MAT)):
		c.writerow(mat[row])
