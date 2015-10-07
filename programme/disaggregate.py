def disaggregate(to_disaggregate, full_results_UP, all_system_scores, all_unit_scores, system_scores, UP_list, Z, 
        disaggregation_criterion, level, check_convergence, CF_categories, impact_method, system_number):
    from scipy.sparse import find
    from numpy import divide
    from copy import copy
    
    lines_before = len(full_results_UP) 
    #number of lines full_results_UP before more are added by this iteration
    
    to_disaggregate_further = [] #this will be the to_disaggregate list for the next level.  It starts empty and will be filled.  
    max_relative = 0.0 #contains the maximum of system score of the lines analized divided by the system score of the whole system
    
    #the convergence check gets closer to 1 at each level.  To keep track of its evolution, each new level starts where the previous one left.  
    check_convergence[level] = copy(check_convergence[level - 1]) 
    for parent_ID in to_disaggregate: #for each parent_ID in the list to disaggregate
        UP_number = full_results_UP[parent_ID]['UP_number']
        parent_demand = full_results_UP[parent_ID]['demand']
        scaling_local = Z[:, UP_number:UP_number+1] * parent_demand #this is the quantity of demand for the new instances
        lines, columns, values = find(scaling_local) #getting rid of all the zeros
        for i in range(len(lines)): #for each new instance number
            #filling the info in full_results_UP
            UP_number = lines[i]
            demand = values[i]
            instance_ID = len(full_results_UP)
            full_results_UP[instance_ID] = {}
            full_results_UP[instance_ID]['instance_ID'] = instance_ID
            full_results_UP[instance_ID]['parent'] = copy(parent_ID)
            full_results_UP[instance_ID]['demand'] = copy(demand)
            full_results_UP[instance_ID]['UP_number'] = copy(UP_number)
            full_results_UP[instance_ID]['pruned'] = 1 #will be changed to 0 if the criterion is not met
            system_scores_revealed = all_system_scores[:, UP_number:UP_number+1] * demand #the system score of the instance
            relative_system_scores = divide(system_scores_revealed, system_scores) #relative system score to the system total
            if max(abs(relative_system_scores)) > disaggregation_criterion: #if the instance maximum relative score is higher than the disaggregation criterion
                to_disaggregate_further.append(instance_ID) #it is added to the list to be further disaggregated
                max_relative = max(max(relative_system_scores), max_relative)
                full_results_UP[instance_ID]['pruned'] = 0
                #the next 2 lines are to fill the check_convergence variable
                relative_contribution = divide(all_unit_scores[:, UP_number:UP_number+1] * demand, system_scores)
                check_convergence[level]['unpruned'] = check_convergence[level]['unpruned'] + relative_contribution
            else: #nothing has to be done if the maximum of relative score is lower than the disaggregation criterion.  Only tracking the convergence.  
                #the next 2 lines are to fill the check_convergence variable
                relative_contribution = divide(system_scores_revealed, system_scores)
                check_convergence[level]['pruned'] = check_convergence[level]['pruned'] + relative_contribution
            check_convergence[level]['sum'] += relative_contribution
    
    #printing on screen the progress of the disaggregation
    for category in CF_categories:
        matrix_line = CF_categories.index(category)
        convergence = check_convergence[level]['sum'][matrix_line, 0]
    
    return full_results_UP, to_disaggregate_further, check_convergence
