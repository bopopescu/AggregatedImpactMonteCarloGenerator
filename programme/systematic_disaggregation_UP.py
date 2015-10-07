def systematic_disaggregation_UP(disaggregation_criterion,full_results_UP, level_reached, system_scores, UP_meta_info, 
        UP_list, EF_list, technology_matrix, intervention_matrix, CF_matrix, CF_categories, EF_unit, 
        uncertainty_info, intensity_matrix, Z, all_system_scores, all_unit_scores, impact_method, final_demand_vector, system_number,systems):
    from calculate_all_scores import calculate_all_scores
    #from write_results_disaggregation_UP import write_results_disaggregation_UP
    from disaggregate import disaggregate
    from initialize_first_level import initialize_first_level
    
    max_level = 25
    max_length = 1e6
    #disaggregation_criterion = 0.1
    
    #calculating unit and system scores of the system to disaggregate
    system_scores, buffer = calculate_all_scores(final_demand_vector, intensity_matrix, intervention_matrix, CF_matrix)
    #the 'buffer' variable is data that wont be used
    
    #Calculation goes like this: the reference flows are disaggregated first.  
    #then, the children of the reference flows that need to be disaggregated will be.  Repeat.  
    #The calculation goes level by level, until there is nothing left to disaggregate.  

    #initializing the first level.  
    #It's different of the rest of the loop because the starting point is the final demand vector
    #the rest of the loop takes the to_disaggregate list instead of the final demand vector.  
    full_results_UP, to_disaggregate, check_convergence = initialize_first_level(all_system_scores, all_unit_scores, 
                                                            system_scores, UP_list, disaggregation_criterion, final_demand_vector, 
                                                            CF_categories, system_number, full_results_UP)
    level = 1
    while 1: #disaggregate until convergence, max_level or max_length is reached.  
        #The disaggregate function is called once per level.  
        full_results_UP, to_disaggregate, check_convergence = disaggregate(to_disaggregate, full_results_UP, all_system_scores, all_unit_scores, 
             system_scores, UP_list, Z, disaggregation_criterion, level, check_convergence, CF_categories, impact_method, system_number)
        if level > max_level or len(full_results_UP) > max_length or len(to_disaggregate) == 0:
            break
        level += 1
    level_reached = level
        
    #write_results_disaggregation_UP(impact_method, full_results_UP, CF_categories, UP_meta_info, UP_list, all_system_scores, all_unit_scores, level_reached, system_scores, system_number,systems)
      
    return full_results_UP, level_reached, system_scores
