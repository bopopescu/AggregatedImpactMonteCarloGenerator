def SimaPro_reader(system_filename, CF_filenames, impact_method):
	import csv
	from capture_UP import capture_UP
	from read_unit_conversion_info import read_unit_conversion_info
	from read_system_meta_info import read_system_meta_info
	from dispatch_meta_info import dispatch_meta_info
	from dispatch_flows import dispatch_flows
	from build_matrices import build_matrices
	from read_CF_IMPACT2002 import read_CF_IMPACT2002
	from build_CF_matrix_IMPACT2002 import build_CF_matrix_IMPACT2002
	from read_CF_Recipe import read_CF_Recipe
	from read_CF_Ecodex import read_CF_Ecodex
	from build_CF_matrix import build_CF_matrix
	from print_CFs import print_CFs
	from read_CF_IMPACT_World import read_CF_IMPACT_World
	from read_CF_IMPACT_World_endpoint import read_CF_IMPACT_World_endpoint
	from read_CF_export import read_CF_export
	from build_CF_matrix_IMPACT_World_endpoint import build_CF_matrix_IMPACT_World_endpoint
	from read_CF_IMPACT_World_terrestrial_acidification import read_CF_IMPACT_World_terrestrial_acidification
	from build_CF_matrix_World_terrestrial_acidification import build_CF_matrix_World_terrestrial_acidification


	infrastructure_rescale = 1e6
    
    #Read information about unit conversion
	unit_converter = read_unit_conversion_info(system_filename)
    
    #reading the few useful meta_informations
	reader = csv.reader(open(system_filename,'U'), delimiter=';')

	system_meta_info = read_system_meta_info(reader)
    
    #Initializing a few variables
	UP_list = []
	EF_list = []
	EF_unit = {}
	all_flow={}
	A = {}
	B = {}
	uncertainty_info = {}
	uncertainty_info['technology'] = {}
	uncertainty_info['intervention'] = {}
	UP_meta_info = {}
    
	while 1:
        #scaning the whole file, UP by UP.  
        #the loop stops if the function capture_UP captured something else than a UP
		all_UP_info = capture_UP(reader)
		if all_UP_info == 'STOP':
			break
		else:
			#the information of each UP is then passed to dispatch_meta_info and 
			#dispatch_flows, to be added to the pre-existing variables
			UP_meta_info, UP_name, all_UP_info = dispatch_meta_info(all_UP_info, UP_meta_info, UP_list, unit_converter)
			UP_list, EF_list,flow_list, A, B , uncertainty_info, EF_unit = dispatch_flows(all_UP_info, UP_name, UP_list, EF_list,all_flow, A, B, 
					uncertainty_info, EF_unit, unit_converter, infrastructure_rescale, UP_meta_info)

	technology_matrix, intervention_matrix = build_matrices(A, UP_list, B, EF_list)
    
	CF_matrices = {}
	CF_categories = {}
	CF_units = {}
    
    
    
	filename = "impact method ecodex.csv"
	reader = csv.reader(open(filename,'U'), delimiter=';')
	(version, CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_export(reader, unit_converter, CF_categories, CF_units)
	CF_matrices = build_CF_matrix(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category, impact_method)
	
	 
	"""
	if impact_method == 'IMPACT World terrestrial acidification':
		#for IW terrestrial acidification per country
		filename = CF_filenames[impact_method]
		CF = read_CF_IMPACT_World_terrestrial_acidification(filename)
		CF_matrices = build_CF_matrix_World_terrestrial_acidification(CF, EF_list, CF_matrices)
	
	if impact_method == 'IMPACT World endpoint':
		filename = CF_filenames[impact_method]
		reader = csv.reader(open(filename,'U'), delimiter=';')
		(CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_IMPACT_World_endpoint(reader, unit_converter, CF_categories, CF_units)
		CF_matrices = build_CF_matrix_IMPACT_World_endpoint(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category)
	if impact_method == 'IMPACT World midpoint':
		filename = CF_filenames[impact_method]
		reader = csv.reader(open(filename,'U'), delimiter=';')
		(CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_IMPACT_World(reader, unit_converter, CF_categories, CF_units)
		CF_matrices = build_CF_matrix(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category, impact_method)
	
	if impact_method == 'IMPACT2002+ midpoint' or impact_method == 'IMPACT2002+ endpoint'or impact_method == 'Climat Change - Impact2002+':
		filename = CF_filenames['IMPACT2002+']
		reader = csv.reader(open(filename,'U'), delimiter=';')
		(CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_IMPACT2002(reader, unit_converter, CF_categories, CF_units)
		CF_matrices = build_CF_matrix_IMPACT2002(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category)
	
		filename = CF_filenames['IMPACT2002+']
		reader = csv.reader(open(filename,'U'), delimiter=';')
		(CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_IMPACT2002(reader, unit_converter, CF_categories, CF_units)
		CF_matrices = build_CF_matrix_IMPACT2002(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category)
	
	if impact_method == 'Recipe midpoint':
		filename = CF_filenames[impact_method]
		reader = csv.reader(open(filename,'U'), delimiter=';')
		(CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_Recipe(reader, unit_converter, CF_categories, CF_units)
		CF_matrices = build_CF_matrix(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category, impact_method)
	
	if impact_method == 'Ecodex':
		filename = CF_filenames[impact_method]
		reader = csv.reader(open(filename,'U'), delimiter=';')
		(version, CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category) = read_CF_Ecodex(reader, unit_converter, CF_categories, CF_units)
		CF_matrices = build_CF_matrix(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category, impact_method)
	
	"""
	
	if 0:
		print_EF_list(EF_list)
		print_CFs(CF_matrices, EF_list, CF_categories)
		print_UP_list(UP_list, UP_meta_info, 0)
        
    #adjusting the unit for infrastructures (they have been rescaled by 1e6)
	for UP_name in UP_meta_info:
		if UP_meta_info[UP_name]['Infrastructure'] == 'Yes':
			UP_meta_info[UP_name]['unit'] = 'micro_' + UP_meta_info[UP_name]['unit']
    
    
	return system_meta_info, UP_meta_info, UP_list, EF_list,all_flow, technology_matrix, intervention_matrix, CF_matrices, CF_categories, CF_units, EF_unit, unit_converter, infrastructure_rescale, uncertainty_info
