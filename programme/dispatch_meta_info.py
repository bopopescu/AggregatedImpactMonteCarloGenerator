def dispatch_meta_info(all_UP_info, UP_meta_info, UP_list, unit_converter):
    from copy import deepcopy
    #the list of marker is different according to the type of UP.  
    #starting with the common markers
    list_markers = ['Category type', 'Process identifier', 'Type', 'Process name', 'Status', 'Time period', 'Geography', 
                    'Technology', 'Representativeness', 'Cut off rules', 'Capital goods', 'Boundary with nature', 
                    'Infrastructure', 'Date', 'Record', 'Generator', 'Litterature references', 'Collection method', 
                    'Data treatment', 'Verification', 'Comment', 'Alloation rules', 'System description']
    UP_type = str(all_UP_info[1][0])
    #adding the ones that are specific
    if UP_type == 'waste treatment':
        list_markers.append('Waste treatment allocation')
        UP_name_marker = 'Waste treatment'
    elif UP_type == 'waste scenario':
        UP_name_marker = 'Waste scenario'
    else:
        UP_name_marker = 'Products'
    
    #scaning all_UP_info for one of the markers
    #when a marker is found, the next line is the information that should be put in UP_meta_info[marker]
    UP_meta_info_transient = {}
    while 1:
        line = all_UP_info.pop(0) #the method pop is used to remove the information.  Once used, it's useless to keep it there
        if len(line) > 0:
            marker = line[0]
        else:
            marker = 'NA'
        if list_markers.count(marker): #if it gives zero, it means the line didn't contain a marker
            line = all_UP_info.pop(0)
            try:
                UP_meta_info_transient[marker] = line[0]
            except IndexError:
                UP_meta_info_transient[marker] = '' #there might be nothing below the marker
        elif marker == UP_name_marker: #catching the UP name
            line = all_UP_info.pop(0)
            UP_name = line[0]
            #catching the country tag            
            
            try:
                UP_meta_info_transient['Country'] = UP_name.split('/')[1].split(' ')[0]
            except IndexError:
                UP_meta_info_transient['Country'] = UP_name.split('{')[-1].split('}')[0]
            except IndexError:
                UP_meta_info_transient['Country'] = 'NA'
           
            if ['m3', 'MJ', '8,'].count(UP_meta_info_transient['Country']): #exceptions for country tag
                UP_meta_info_transient['Country'] = UP_name.split('/')[1].split(' ')[0]
           
            print UP_meta_info_transient['Country'],
            print UP_name
            raw_input()
                    
            #putting the first level of category type in a list
            UP_meta_info_transient['Category type'] = [UP_meta_info_transient['Category type']]
            if marker == 'Products': #the rest of the category are at different places according to process type
                try:
                    UP_meta_info_transient['Category type'].extend(line[5].split('\\'))
                except IndexError:
                    1
            elif marker == 'Waste treatment':
                try:
                    UP_meta_info_transient['Category type'].extend(line[4].split('\\'))
                except IndexError:
                    1
            UP_meta_info_transient['scaling factor'] = unit_converter[line[1]][1] #this info is necessary to scale the whole column afterward
            UP_meta_info_transient['unit'] = unit_converter[line[1]][0]
            try: #if the UP_name is not already existing, add it to the list
                UP_list.index(UP_name)
            except ValueError:
                UP_list.append(UP_name)
            all_UP_info.pop(0) #empty line between the product name and "Avoided products"
            break #after that point, the information has to be dispatched in matrices.  This is done in other functions
    
    UP_meta_info[UP_name] = deepcopy(UP_meta_info_transient)
    return UP_meta_info, UP_name, all_UP_info
