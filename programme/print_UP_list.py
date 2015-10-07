def print_UP_list(UP_list, UP_meta_info, base):
    from openpyxl.workbook import Workbook
    from openpyxl.worksheet import Worksheet
    
    filename = 'UP_print.xlsx'
    wb = Workbook(encoding='mac_roman')
    ws = Worksheet(wb, title = 'UP_list') #creating a sheet inside the workbook
    ws.freeze_panes = 'A2'
    header = ['#', 
              'UP name', 
              'unit', 
              'country', 
              'infrastructure']
    for i in range(6):
        header.append('Category ' + str(i))
    ws.append(header)
    
    for i in range(len(UP_list)):
        UP = UP_list[i]
        line = [i + base, 
                UP_list[i], 
                UP_meta_info[UP]['unit'], 
                UP_meta_info[UP]['Country'], 
                UP_meta_info[UP]['Infrastructure']]
        for j in range(6):
            try:
                line.append(UP_meta_info[UP]['Category type'][j])
            except IndexError:
                break
        ws.append(line)
    print 'saving in excel sheet named: ' + filename
    wb.add_sheet(ws)
    wb.save(filename)
