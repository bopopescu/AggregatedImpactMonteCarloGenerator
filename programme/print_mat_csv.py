def print_mat(MAT,nom):
	from numpy import array
	import csv

	c = csv.writer(open(nom+".csv", "wb"))
		
	mat=array(MAT)
	for row in range(len(mat)):
		c.writerow(mat[row])
