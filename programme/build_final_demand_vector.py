def build_final_demand_vector(system, UP_list):
    from numpy import matrix, zeros
    
    final_demand_vector = matrix(zeros((len(UP_list),1)))
    for UP in system:
        matrix_line = UP_list.index(UP)
        final_demand_vector[matrix_line, 0] = system[UP]
    
    return final_demand_vector