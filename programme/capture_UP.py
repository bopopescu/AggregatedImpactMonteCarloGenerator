def capture_UP(reader):
    
    stop = 0
    while 1: #positionning the reader where the UP info starts
        line = next(reader)
        if len(line) > 0:
            if line[0] == 'Process':
                break
        #the keyword 'System description' appears in the middle of a UP, but never to start a UP
        #bumping on this keyword at the beginning means that the UP are done reading
        if len(line) > 0:
            if line[0] == 'System description': 
                all_UP_info = 'STOP'
                stop = 1
                break
    
    if stop == 0:
        all_UP_info = []
        next(reader) #skipping an empty line
        while 1: #keep scaning until the word "End" is met
            line = next(reader)
            if len(line) > 0:
                if line[0] == 'End': #every UP ends with the "End" marker
                    break
                else:
                    all_UP_info.append(line)
            else:
                all_UP_info.append([])
    
    return all_UP_info
