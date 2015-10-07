def write_results_disaggregation_UP(impact_method, full_results_UP, CF_categories, UP_meta_info, UP_list, all_system_scores, 
        all_unit_scores, level_reached, system_scores, system_number,systems):
    from openpyxl.workbook import Workbook
    from openpyxl.worksheet import Worksheet
    from construct_path import construct_path
    from copy import copy
    
    filename = 'disaggregation_' + impact_method + '_system' + str(system_number) + '.xlsx'
    wb = Workbook(encoding = 'mac_roman') #creating a workbook
    ws = Worksheet(wb, title = 'result') #creating a sheet inside the workbook
    
    #creation of headers
    header2 = ['instance ID', 
              'parent instance ID', 
              'unit process', 
              'demand', 
              'unit', 
              'pruned',
              'level', 
              'infrastructure']
    for impact_category in CF_categories:
        header2.append(impact_category)
    for i in range(1, level_reached + 1):
        header2.append('path level ' + str(i))
    header2.append('country')
    for i in range(4):
        header2.append('category ' + str(i))
    
    header1 = []
    for i in range(header2.index(CF_categories[0])):
        header1.append('')
    for impact_category in CF_categories:
        matrix_line = CF_categories.index(impact_category)
        header1.append(str(system_scores[matrix_line,0]))
    ws.append(header1) #writing the header
    ws.append(header2) #writing the header
    
    #content of the file
    for instance_ID in range(len(full_results_UP)): #for each instance of the full_results
        path = construct_path(full_results_UP, instance_ID, UP_list, impact_method, system_number) #construction of the path between the instance and the RF
        level = len(path) - 1 #level will be incremented from zero
        matrix_column = full_results_UP[instance_ID]['UP_number']
        UP_name = UP_list[matrix_column]
        demand = copy(full_results_UP[instance_ID]['demand'])
        #fetching the info to fill the line
        line = [instance_ID, 
                full_results_UP[instance_ID]['parent'], 
                UP_name, 
                demand, 
                UP_meta_info[UP_name]['unit'], 
                full_results_UP[instance_ID]['pruned'], 
                level, 
                UP_meta_info[UP_name]['Infrastructure']]
        for impact_category in CF_categories: #system or unit scores.  
            matrix_line = CF_categories.index(impact_category)
            if full_results_UP[instance_ID]['pruned'] == 1:
                line.append(all_system_scores[matrix_line, matrix_column] * demand)
            else:
                line.append(all_unit_scores[matrix_line, matrix_column] * demand)
        for i in range(1, level_reached + 1): #path
            try:
                line.append(path[i])
            except IndexError:
                line.append('')
        #complementary info
        line.append(UP_meta_info[UP_name]['Country'])
        for i in range(4):
            try:
                line.append(UP_meta_info[UP_name]['Category type'][i])
            except IndexError:
                line.append('')
        #print line
        ws.append(line) #writing the header
    ws.freeze_panes = 'D3'
    wb.add_sheet(ws)
    wb.save(filename)
