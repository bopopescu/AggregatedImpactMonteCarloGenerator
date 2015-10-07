def fix_inverse(Z, inverse_technology_matrix):
    from numpy import zeros, shape, sum
    #because of poor conditionning (?), the inverse will contain coefficients that should not be there.  
    #in the z matrix, if a line or a column contains only zero elements, the inverse should
    #contain only zero elements as well, except for the main diagonal.  
    #this function will force these coefficients to zero if they are not.  
    
    
    for i in range(shape(Z)[0]):
        if sum(Z[:,i].todense()) == 0.0:
            inverse_technology_matrix[:,i:i+1] = zeros((shape(Z)[0], 1))
            inverse_technology_matrix[i,i] = 1.0
        if sum(Z[i,:].todense()) == 0.0:
            inverse_technology_matrix[i:i+1,:] = zeros((1, shape(Z)[0]))
            inverse_technology_matrix[i,i] = 1.0
    
    return inverse_technology_matrix
