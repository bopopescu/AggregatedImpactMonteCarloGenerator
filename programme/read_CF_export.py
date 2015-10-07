def read_CF_export(reader, unit_converter, CF_categories, CF_units):
	
	version=""
	
	line = next(reader)
	if 1:#line[0][1:10]=="SimaPro 8":
		line = next(reader)
		if line[0]=="{methods}":
			while 1:
				line = next(reader)
				if len(line)>0:
					if line[0]=="End":
						break 
					if line[0]=="Name":
						impact_method=next(reader)[0]
						CF_categories[impact_method] = []
						CF_units[impact_method] = []
						EF_list_for_CF_global = []
						EF_list_for_CF_per_category = {} 
						#a list per category is necessary for a reason that will become apparent when it's time to
						#match EF of the DB with their CF
						H = []
						dammage_factors = {}
					if line[0]=="Version":
						version=",".join(next(reader))
					if line[0] == 'Impact category': #this is the sign of a new category
						line=next(reader)
						category = line[0]
						unit = line[1]
						CF_categories[impact_method].append(category)
						CF_units[impact_method].append(unit)
						matrix_line = CF_categories[impact_method].index(category) #each line of the H matrix is a category
						EF_list_for_CF_per_category[category] = []
						line=next(reader)
						line=next(reader)
						while 1: #read the list of CFs until the next break
							line = next(reader)
							if len(line) == 0:
								break
							else:
								[compartment, sub_compartment, EF, CAS, CF, unit] = line #info is regularly placed
								if compartment == 'Raw':
									compartment = 'Resources' #to be consistent with the DB
								EF_list_for_CF_per_category[category].append([compartment, EF, sub_compartment]) #in this list, EF only appear once and in order
								if EF_list_for_CF_global.count([compartment, EF, sub_compartment]) == 0: #if the EF does not exist in the list
									EF_list_for_CF_global.append([compartment, EF, sub_compartment]) #add it
								matrix_column = EF_list_for_CF_global.index([compartment, EF, sub_compartment]) #find the EF number in the list
								H.append([matrix_line, matrix_column, float(CF.replace(',','.'))])

			return version, CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category

if __name__=="__main__":
	from read_unit_conversion_info import read_unit_conversion_info
	import csv
	
	system_filename = "export_7_3_2.csv"
	CF_categories={}
	CF_units={}
	
	unit_converter = read_unit_conversion_info(system_filename)
	reader = csv.reader(open("impact method ecodex.csv",'U'), delimiter=';')
	read_CF_export(reader, unit_converter, CF_categories, CF_units)
	
