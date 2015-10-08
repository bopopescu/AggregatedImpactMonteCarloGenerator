def read_CF_export_7(reader, unit_converter, CF_categories, CF_units):
    
	version=""
	
	line = next(reader)
	if 1:#line[0][1:10]=="SimaPro 7":
		if line[1]=="method":
			while 1:
				try:
					line = next(reader)
				except:
					print line
					raw_input()
				if len(line)>0:
					if line[0]=="End":
						break 
					if line[0]=="Name":
						impact_method=line[1]
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
						category = line[1]
						unit=line[2]
						CF_categories[impact_method].append(category)
						CF_units[impact_method].append(unit)
						matrix_line = CF_categories[impact_method].index(category) #each line of the H matrix is a category
						EF_list_for_CF_per_category[category] = []
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
					
					elif line[0] == 'Damage category': #fetching the factors to go from midpoint to endpoint
						if not impact_method+"-dammages" in CF_categories:
							CF_categories[impact_method+"-dammages"] = []
							CF_units[impact_method+"-dammages"] = []
						endpoint_category = line[1]
						endpoint_unit=line[2]
						CF_categories[impact_method+"-dammages"].append(endpoint_category)
						CF_units[impact_method+"-dammages"].append(endpoint_unit)
						dammage_factors[endpoint_category] = {}
						while 1:
							line = next(reader)
							if len(line) == 0:
								break
							else:
								midpoint_category = line[0]
								factor = line[1]
								dammage_factors[endpoint_category][midpoint_category] = float(factor.replace(',','.'))
		
	return version, CF_categories,CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category

if __name__=="__main__":
	from read_unit_conversion_info import read_unit_conversion_info
	import csv
	
	system_filename = "ecoinvent_v22.CSV"
	CF_categories={}
	CF_units={}
	
	unit_converter = read_unit_conversion_info(system_filename)
	reader = csv.reader(open("IMPACT2002 update 2011.csv",'U'), delimiter=';')
	read_CF_IMPACT2002(reader, unit_converter, CF_categories, CF_units)
	
