def read_CF_Recipe(reader, unit_converter, CF_categories, CF_units):
    
    #the file contains the CF for midpoint and the factors to go from midpoint to endpoint
    #we can create 3 impact methods with it: midpoint, endpoint, and midpoint with endpoint units
    CF_categories['Recipe midpoint'] = []
    CF_units['Recipe midpoint'] = []
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
                    unit = line[2]
                    CF_categories['Recipe midpoint'].append(category)
                    CF_units['Recipe midpoint'].append(unit)
                    matrix_line = CF_categories['Recipe midpoint'].index(category) #each line of the H matrix is a category
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
        except StopIteration:
            break
    
    return CF_categories, CF_units, dammage_factors, H, EF_list_for_CF_global, EF_list_for_CF_per_category
