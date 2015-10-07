def treat_economic_flow_info(flow, column_number, UP_list, sign, A, UP_scaling_factor, unit_converter, 
                             marker, uncertainty_info, infrastructure_rescale, UP_meta_info):
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
    
    #if the UP is not in the list yet, add it
    try:
        UP_list.index(UP_name)
    except ValueError:
        UP_list.append(UP_name)
    
    #raising a warning if a process calls itself
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
    try: #sometimes, a process is called several times.  In this case, the coefficient should be added to the existing one
        A[column_number][line_number] += coefficient
        #if there is no error, it means this line already exists.  
        if (spread1 > uncertainty_info['technology'][column_number][line_number]['spread1'] or 
            spread2 > uncertainty_info['technology'][column_number][line_number]['spread2'] or 
            spread3 > uncertainty_info['technology'][column_number][line_number]['spread3']):
            #if the uncertainty of the new one is bigger, the uncertainty info of the new one is
            #reatined, just to be on the safe side.  
            uncertainty_info['technology'][column_number][line_number]['distribution'] = distribution
            uncertainty_info['technology'][column_number][line_number]['spread1'] = spread1
            uncertainty_info['technology'][column_number][line_number]['spread2'] = spread2
            uncertainty_info['technology'][column_number][line_number]['spread3'] = spread3
            if pedigree != '':
                uncertainty_info['technology'][column_number][line_number]['pedigree'] = treat_pedigree(pedigree)
    except KeyError: #the process has been called for the first time, so the info has to be created from scratch
        A[column_number][line_number] = coefficient
        uncertainty_info['technology'][column_number][line_number] = {}
        uncertainty_info['technology'][column_number][line_number]['distribution'] = distribution
        uncertainty_info['technology'][column_number][line_number]['spread1'] = spread1
        uncertainty_info['technology'][column_number][line_number]['spread2'] = spread2
        uncertainty_info['technology'][column_number][line_number]['spread3'] = spread3
        if pedigree != '':
            uncertainty_info['technology'][column_number][line_number]['pedigree'] = treat_pedigree(pedigree)
    
    return UP_list, A, uncertainty_info
