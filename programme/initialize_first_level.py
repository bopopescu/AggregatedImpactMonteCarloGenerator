def initialize_first_level(all_system_scores, all_unit_scores, system_scores, UP_list, disaggregation_criterion, 
        final_demand_vector, CF_categories, system_number, full_results_UP):
    from scipy.sparse import find
    from numpy import divide, zeros, shape
    from copy import copy
    
    #see the function disaggregate for more comment.  Similar principles.  
    level = 0
    check_convergence = {}
    check_convergence[level] = {}
    check_convergence[level]['pruned'] = zeros((shape(all_system_scores)[0], 1))
    check_convergence[level]['unpruned'] = zeros((shape(all_system_scores)[0], 1))
    check_convergence[level]['sum'] = zeros((shape(all_system_scores)[0], 1))
    to_disaggregate_further = []
    max_relative = 0.0
    lines, columns, values = find(final_demand_vector)
    for i in range(len(lines)):
        UP_number = lines[i]
        demand = values[i]
        instance_ID = copy(i)
        full_results_UP[instance_ID] = {}
        full_results_UP[instance_ID]['instance_ID'] = instance_ID
        full_results_UP[instance_ID]['parent'] = 'RF'
        full_results_UP[instance_ID]['demand'] = copy(demand)
        full_results_UP[instance_ID]['UP_number'] = copy(UP_number)
        full_results_UP[instance_ID]['pruned'] = 1 #will be changed to 0 if the criterion is not met
        system_scores_revealed = all_system_scores[:, UP_number:UP_number+1] * demand

        relative_system_scores = divide(system_scores_revealed, system_scores)
        if max(abs(relative_system_scores)) > disaggregation_criterion:
            to_disaggregate_further.append(instance_ID)
            max_relative = max(abs(max(relative_system_scores)), max_relative)
            full_results_UP[instance_ID]['pruned'] = 0
            relative_contribution = divide(all_unit_scores[:, UP_number:UP_number+1] * demand, system_scores)
            check_convergence[level]['unpruned'] = check_convergence[level]['unpruned'] + relative_contribution
        else:
            relative_contribution = divide(system_scores_revealed, system_scores)
            check_convergence[level]['pruned'] = check_convergence[level]['pruned'] + relative_contribution
        check_convergence[level]['sum'] = check_convergence[level]['sum'] + relative_contribution
    for category in CF_categories:
        matrix_line = CF_categories.index(category)
        convergence = check_convergence[level]['sum'][matrix_line, 0]
    
    return full_results_UP, to_disaggregate_further, check_convergence
