def read_CF_IMPACT_World_terrestrial_acidification(filename):
    from openpyxl.reader.excel import load_workbook
    
    print 'loading ' + filename
    wb = load_workbook(filename)
    
    ws = wb.get_sheet_by_name('Feuil2')
    translation = {}
    for row in ws.rows:
        name_in_method = str(row[0].value)
        name_in_DB = str(row[1].value)
        translation[name_in_method] = name_in_DB
        
    ws = wb.get_sheet_by_name('Feuil1')
    
    print 'reading CF for each country'
    headers = {}
    for line in [0, 1]:
        row = ws.rows[line]
        headers[line] = []
        for column in range(len(row)):
            headers[line].append(str(row[column].value))
    
    CF = {}
    for row in ws.rows[2:]:
        country = str(row[0].value)
        CF[country] = {}
        CF[country]['midpoint'] = {}
        CF[country]['endpoint'] = {}
        for column in range(1, len(row)):
            mid_end = headers[0][column]
            substance = translation[headers[1][column]]
            CF[country][mid_end][substance] = float(row[column].value)
    
    return CF