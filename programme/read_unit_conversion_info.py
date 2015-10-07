def read_unit_conversion_info(system_filename):
    import csv
    reader = csv.reader(open(system_filename,'U'), delimiter=';')
    #reading data about unit conversion
    #positionning the reader on the line with the first cell containing "Units"
    while 1:
        line = next(reader)
        if len(line) > 0:
            if line[0] == 'Units': 
                break

    #the unit converter takes a unit as an input and gives a
    #reference unit with a conversion factor.  
    #conversion_factor = # of reference_unit per starting_unit.  
    #Exemple: 
    #starting_unit = 'g'
    #reference_unit = 'kg'
    #conversion_factor = how many kg per g? = 0.001
    unit_converter = {}
    while 1:
        line = next(reader)
        if len(line) > 0:
            starting_unit = str(line[0])
            convertion_factor = float(line[2].replace(',','.'))
            reference_unit = str(line[3])
            unit_converter[starting_unit] = [reference_unit, convertion_factor]
        else:
            break
    
    return unit_converter