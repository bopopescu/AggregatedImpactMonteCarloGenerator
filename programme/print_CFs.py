def print_CFs(CF_matrices, EF_list, CF_categories):
    from openpyxl.workbook import Workbook
    from openpyxl.worksheet import Worksheet
    
    result_filename = 'CF_print.xlsx'
    wb = Workbook() #creating a workbook
    for method in CF_matrices:
        ws = Worksheet(wb, title = method) #creating a sheet inside the workbook
        ws.freeze_panes = 'D2'
        header = ['compartment', 
              'substance', 
              'subcompartment']
        for category in CF_categories[method]:
            header.append(category)
        ws.append(header)
        for EF in EF_list:
            matrix_column = EF_list.index(EF)
            compartment, substance, subcompartment = EF
            line = [compartment, substance, subcompartment]
            for category in CF_categories[method]:
                matrix_line = CF_categories[method].index(category)
                CF = CF_matrices[method][matrix_line, matrix_column]
                line.append(CF)
            ws.append(line)
    print 'saving in excel sheet named: ' + result_filename
    wb.add_sheet(ws)
    wb.save(result_filename)