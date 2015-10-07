def print_result(impacts,systems, system_number,UP_list):
	import csv
	for UP in systems[system_number]:    
		name=UP_list.index(UP)
		c = csv.writer(open(str(name)+".csv", "wb"))
		c.writerow([UP])
		header = ['CC', 'HH', 'EQ', 'RR', 'WW']
		c.writerow(header)
	
	for row in range(len(impacts)):
		c.writerow(impacts[row])
