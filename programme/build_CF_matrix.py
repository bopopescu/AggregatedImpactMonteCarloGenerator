def build_CF_matrix(CF_categories, dammage_factors, H, EF_list_for_CF_global, EF_list, 
                           CF_matrices, EF_list_for_CF_per_category, impact_method):
    from scipy.sparse import lil_matrix, find
    from copy import deepcopy
    
    #building a transient matrix (the columns correspond to the system set up by the impact method, NOT the one of ecoinvent)
    transient_CF = lil_matrix((len(CF_categories[impact_method]), len(EF_list_for_CF_global)))
    for [matrix_line, matrix_column, CF] in H:
        transient_CF[matrix_line, matrix_column] = CF
    
    #building the matrix
    CF_matrices[impact_method] = lil_matrix((len(CF_categories[impact_method]), len(EF_list)))
    for category in CF_categories[impact_method]:
        matrix_line = CF_categories[impact_method].index(category)
        for EF in EF_list:
            column_number_EF = EF_list.index(EF)
            if EF_list_for_CF_per_category[category].count(EF): #if the exact EF is found in the list of EF with a CF in this specefic category
                column_number_CF = EF_list_for_CF_global.index(EF) #find the number in the global list
            else:
                EF_transient = deepcopy(EF)
                EF_transient[2] = '(unspecified)'
                #a EF without exact match will recieve the (unspecified) CF if compartment and EF ID match
                if EF_list_for_CF_per_category[category].count(EF_transient):
                    column_number_CF = EF_list_for_CF_global.index(EF_transient)
                else: #otherwise, no match, the CF is left to zero
                    column_number_CF = 'NA'
            if column_number_CF != 'NA':
                CF_matrices[impact_method][matrix_line, column_number_EF] = transient_CF[matrix_line, column_number_CF]
    del transient_CF
    
    del H, EF_list_for_CF_global, EF_list_for_CF_per_category, dammage_factors

    return CF_matrices
    
