def treat_elementary_flow_info(flow, column_number, EF_list, B, UP_scaling_factor, 
                               unit_converter, compartment, uncertainty_info, EF_unit, UP_list):
    from treat_pedigree import treat_pedigree
    #for more comment, see treat_economic_flow_info, the structure is the same.  
    
    EF_name = flow[0]
    sub_compartment = flow[1]
    if sub_compartment == '':
        sub_compartment = '(unspecified)'
    unit = flow[2]
    coefficient = float(flow[3].replace(',','.'))
    distribution = flow[4]
    spread1 = float(flow[5].replace(',','.'))
    spread2 = float(flow[6].replace(',','.'))
    spread3 = float(flow[7].replace(',','.'))
    
    try:
        pedigree = flow[8]
    except IndexError:
        pedigree = ''
    
    try:
        EF_list.index([compartment, EF_name, sub_compartment])
    except ValueError:
        EF_list.append([compartment, EF_name, sub_compartment])
        EF_unit[EF_name] = unit_converter[unit][0]
    line_number = EF_list.index([compartment, EF_name, sub_compartment])
    coefficient = float(coefficient) * unit_converter[unit][1] / UP_scaling_factor
    if distribution=="Normal":
		spread1 = float(spread1) * unit_converter[unit][1] / UP_scaling_factor
    try:
        B[column_number][line_number] += coefficient
        #if there is no error, it means this line already exists.  
        if (spread1 > uncertainty_info['intervention'][column_number][line_number]['spread1'] or 
            spread2 > uncertainty_info['intervention'][column_number][line_number]['spread2'] or 
            spread3 > uncertainty_info['intervention'][column_number][line_number]['spread3']):
            #if the uncertainty of the new one is bigger, the uncertainty info of the new one is
            #reatined, just to be on the safe side.  
            uncertainty_info['intervention'][column_number][line_number]['distribution'] = distribution
            uncertainty_info['intervention'][column_number][line_number]['spread1'] = spread1
            uncertainty_info['intervention'][column_number][line_number]['spread2'] = spread2
            uncertainty_info['intervention'][column_number][line_number]['spread3'] = spread3
            if pedigree != '':
                uncertainty_info['intervention'][column_number][line_number]['pedigree'] = treat_pedigree(pedigree)
    except KeyError:
        B[column_number][line_number] = coefficient
        uncertainty_info['intervention'][column_number][line_number] = {}
        uncertainty_info['intervention'][column_number][line_number]['distribution'] = distribution
        uncertainty_info['intervention'][column_number][line_number]['spread1'] = spread1
        uncertainty_info['intervention'][column_number][line_number]['spread2'] = spread2
        uncertainty_info['intervention'][column_number][line_number]['spread3'] = spread3
        if pedigree != '':
            uncertainty_info['intervention'][column_number][line_number]['pedigree'] = treat_pedigree(pedigree)
    
    return EF_list, B, uncertainty_info, EF_unit
