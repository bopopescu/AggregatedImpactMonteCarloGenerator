def calculate_all_scores(final_demand_vector, intensity_matrix, intervention_matrix, CF_matrix):
    unit_scores = CF_matrix * intervention_matrix.todense()*final_demand_vector
    system_scores = CF_matrix * intensity_matrix * final_demand_vector
    return system_scores, unit_scores
