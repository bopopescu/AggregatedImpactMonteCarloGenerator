def read_list_UP_desag(reader):
    from openpyxl.reader.excel import load_workbook
    print 'reading unit process to analyse in file ' + reader
    print ''
    wb = load_workbook(reader)
    ws = wb.get_sheet_by_name('result')
            
    UP_list_desag = []
    header = 1
    for row in ws.rows:
        if header == 1:
            header = 0
        else:
            UP_name = str(row[2])
            UP_list_desag.append(UP_name)
    
    return UP_list_desag
