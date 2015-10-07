def read_CSV(filename):
	import csv
	from numpy import loadtxt, array
    
	sample = loadtxt(filename, delimiter = ',')
	#reader = csv.reader(open(filename, 'r'))
	#sample = []
	#for row in reader:
		#sample.append(row)

	return array(sample)
