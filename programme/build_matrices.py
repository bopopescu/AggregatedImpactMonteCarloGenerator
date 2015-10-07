def build_matrices(A, UP_list, B, EF_list):
    from scipy.sparse import lil_matrix, find, csr_matrix, csc_matrix
    from print_mat import print_mat
    
    technology_matrix = lil_matrix((len(UP_list), len(UP_list)))
    
    for column in A:
        for line in A[column]:
            technology_matrix[line, column] += A[column][line]
    
    #in case there are UP demanded but not supplied by the database, the column is null.  This has to be fixed
    for UP in UP_list:
        matrix_column = UP_list.index(UP)
        if technology_matrix[matrix_column,matrix_column] == 0.0:
            print 'warning: ' + UP + ' was excluded from the project: consider re-exporting'
            technology_matrix[matrix_column, matrix_column] = 1.0
    
    intervention_matrix = lil_matrix((len(EF_list), len(UP_list)))
    for column in B:
        for line in B[column]:
            intervention_matrix[line, column] += B[column][line]
    
    return technology_matrix, intervention_matrix
