def read_CF_IMPACT2002(reader, unit_converter, CF_categories, CF_units):
    
    #the file contains the CF for midpoint and the factors to go from midpoint to endpoint
    #we can create 3 impact methods with it: midpoint, endpoint, and midpoint with endpoint units
    CF_categories['IMPACT2002+ midpoint'] = []
    CF_categories['IMPACT2002+ mid_end'] = []
    CF_categories['IMPACT2002+ endpoint'] = []
    CF_units['IMPACT2002+ midpoint'] = []
    CF_units['IMPACT2002+ mid_end'] = []
    CF_units['IMPACT2002+ endpoint'] = []
    EF_list_for_CF_global = []
    EF_list_for_CF_per_category = {} 
    #a list per category is necessary for a reason that will become apparent when it's time to
    #match EF of the DB with their CF
    H = []
    dammage_factors = {}
    while 1: #scaning the whole file until the end
        try:
            line = next(reader)
            if len(line) > 0:
                if line[0] == 'Impact category': #this is the sign of a new category
                    category = line[1]
                    unit=line[2]
                    CF_categories['IMPACT2002+ midpoint'].append(category)
                    CF_categories['IMPACT2002+ mid_end'].append(category)
                    CF_units['IMPACT2002+ midpoint'].append(unit)
                    CF_units['IMPACT2002+ mid_end'].append(unit)
                    matrix_line = CF_categories['IMPACT2002+ midpoint'].index(category) #each line of the H matrix is a category
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
                    endpoint_category = line[1]
                    endpoint_unit=line[2]
                    CF_categories['IMPACT2002+ endpoint'].append(endpoint_category)
                    CF_units['IMPACT2002+ endpoint'].append(endpoint_unit)
                    dammage_factors[endpoint_category] = {}
                    while 1:
                        line = next(reader)
                        if len(line) == 0:
                            break
                        else:
                            midpoint_category = line[0]
                            factor = line[1]
                            dammage_factors[endpoint_category][midpoint_category] = float(factor.replace(',','.'))
        except StopIteration:
            break
    
    return CF_categories,CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category
