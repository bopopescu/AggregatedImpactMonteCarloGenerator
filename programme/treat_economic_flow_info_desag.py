def treat_economic_flow_info_desag(flow,UP, column_number, UP_list, sign, A, UP_scaling_factor, unit_converter, 
                             marker, uncertainty_info, infrastructure_rescale, UP_meta_info,UP_list_desag_1):
    from treat_pedigree import treat_pedigree

    UP_name = flow[0]
    coefficient = float(flow[2].replace(',','.'))
    if marker == 'Remaining waste' or marker == 'Separated waste': #these flow display less info
        unit = 'kg'
        distribution = 'NA'
        spread1 = 'NA'
        spread2 = 'NA'
        spread3 = 'NA'
    else: #otherwise, the unit, distribution and spreads are in regular places
        unit = flow[1]
        distribution = flow[3]
        spread1 = float(flow[4].replace(',','.'))
        spread2 = float(flow[5].replace(',','.'))
        spread3 = float(flow[6].replace(',','.'))
    try:
        pedigree = flow[7]
    except IndexError:
        pedigree = ''
    """
    #raising a warning if a process calls itself
    for process in UP_list_desag_1:
		if UP_list[UP_list_desag_1[process]['UP_number']]==UP_name:
			line_number=UP_list_desag_1[process]['instance_ID']
    """
		
    line_number = UP_list.index(UP_name)
    if line_number == column_number:
        print 'alert! UP is calling itself:'
        print line_number
        print UP_list[line_number]
        print ''
    
    #adjusting the coefficient for unit consistency.  
    #Two conversions have to be made: one for the process calling, and one for the process being called
    coefficient = float(coefficient) * unit_converter[unit][1] / UP_scaling_factor * sign
    if UP_name.find('/I ') != -1: #if the process does NOT NOT contains the infrastructure chain of character, rescale it
        coefficient = coefficient * infrastructure_rescale
        
    A[column_number][line_number] = coefficient
    uncertainty_info['technology'][column_number][line_number] = {}
    uncertainty_info['technology'][column_number][line_number]['distribution'] = distribution
    uncertainty_info['technology'][column_number][line_number]['spread1'] = spread1
    uncertainty_info['technology'][column_number][line_number]['spread2'] = spread2
    uncertainty_info['technology'][column_number][line_number]['spread3'] = spread3
    if pedigree != '':
        uncertainty_info['technology'][column_number][line_number]['pedigree'] = treat_pedigree(pedigree)
    
    return UP_list, A, uncertainty_info
