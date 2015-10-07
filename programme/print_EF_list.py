def print_EF_list(EF_list):
    from openpyxl.workbook import Workbook
    from openpyxl.worksheet import Worksheet
    
    result_filename = 'EF_print.xlsx'
    wb = Workbook() #creating a workbook
    ws = Worksheet(wb, title = 'EF_list') #creating a sheet inside the workbook
    ws.freeze_panes = 'A2'
    header = ['compartment', 
          'substance', 
          'subcompartment']
    ws.append(header)
    for EF in EF_list:
        ws.append(EF)
    print 'saving in excel sheet named: ' + result_filename
    wb.add_sheet(ws)
    wb.save(result_filename)