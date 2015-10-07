def build_CF_matrix_IMPACT_World_endpoint(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, CF_matrices, EF_list_for_CF_per_category):
    from scipy.sparse import lil_matrix, find
    from copy import deepcopy

    #building a transient matrix (the columns correspond to the system set up by the impact method, NOT the one of ecoinvent)
    transient_CF = lil_matrix((len(CF_categories['IMPACT World mid_end']), len(EF_list_for_CF_global)))
    for [matrix_line, matrix_column, CF] in H:
        transient_CF[matrix_line, matrix_column] = CF
    
    #building the matrix for midpoint
    CF_matrices['IMPACT World mid_end'] = lil_matrix((len(CF_categories['IMPACT World mid_end']), len(EF_list)))
    for category in CF_categories['IMPACT World mid_end']:
        matrix_line = CF_categories['IMPACT World mid_end'].index(category)
        for EF in EF_list:
            column_number_EF = EF_list.index(EF)
            if EF_list_for_CF_per_category[category].count(EF): #if the exact EF is found in the list of EF with a CF in this specefic category
                column_number_CF = EF_list_for_CF_global.index(EF) #find the number in the global list
            else:
                EF_transient = deepcopy(EF)
                EF_transient[2] = '(unspecified)'
                if EF_list_for_CF_per_category[category].count(EF_transient): #a EF without exact match will recieve the (unspecified) CF if compartment and EF ID match
                    column_number_CF = EF_list_for_CF_global.index(EF_transient)
                else: #otherwise, no match, the CF is left to zero
                    column_number_CF = 'NA'
            if column_number_CF != 'NA':
                CF_matrices['IMPACT World mid_end'][matrix_line, column_number_EF] = transient_CF[matrix_line, column_number_CF]
    del transient_CF
    
    #building the matrix for endpoint
    #each line in the matrix is the sum of one or more lines in CF_categories['IMPACT World mid_end']
    CF_matrices['IMPACT World endpoint'] = lil_matrix((len(CF_categories['IMPACT World endpoint']), len(EF_list)))
    for endpoint_category in dammage_factors:
        matrix_line_endpoint = CF_categories['IMPACT World endpoint'].index(endpoint_category)
        for midpoint_category in dammage_factors[endpoint_category]:
            matrix_line_midpoint = CF_categories['IMPACT World mid_end'].index(midpoint_category)
            #start with a null line, and add all the relevant lines from CF_categories['IMPACT World mid_end']
            CF_matrices['IMPACT World endpoint'][matrix_line_endpoint, :] = (CF_matrices['IMPACT World endpoint'][matrix_line_endpoint, :] + 
                                                                            CF_matrices['IMPACT World mid_end'][matrix_line_midpoint, :])
    
    del H, EF_list_for_CF_global, EF_list_for_CF_per_category, dammage_factors

    return CF_matrices
