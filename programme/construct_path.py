def construct_path(full_results_UP, instance_ID, UP_list, impact_method, system_number):
    from copy import copy
    
    #the path is constructed in reverse order, from the instance to the RF.  
    #the link between each element is found through the parent
    path = []
    local_instance = copy(instance_ID)
    while 1:
        parent_ID = full_results_UP[local_instance]['parent']
        try:
            UP_number = full_results_UP[parent_ID]['UP_number']
            UP_name = UP_list[UP_number]
            path.append(UP_name)
            local_instance = copy(full_results_UP[local_instance]['parent'])
        except KeyError:
            path.append('RF')
            break
    path.reverse()
    
    return path
