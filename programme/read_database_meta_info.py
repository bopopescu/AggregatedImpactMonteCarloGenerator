def read_database_meta_info(filename):
    import csv
    
    reader = csv.reader(open(filename,'U'), delimiter=';')
    #the first few lines of the file are not very useful.  
    #only fetching the project name and decimal separator
    system_meta_info = {}
    line = next(reader) #{SimaPro 7.*} or {SimaPro 8.*}
    if line[0][1:10]=="Simapro 8":
		data_type = next(reader)[0][1:-1]
		while 1:
			line = next(reader)
			if len(line)>0:
				if line[0]=="Name":
					database_name=next(reader)[0]
				if line[0]=="Version":
					database_version=next(reader).join(".")
    next(reader) #{processes} or {method}
    next(reader) #{Date: 2/23/2012}
    next(reader) #{Time: 12:47:38 PM}
    line = next(reader) #{Project: tutoriel_GCH6310}
    system_meta_info['project_name'] = line[0][10:-1]
    next(reader) #{CSV Format version: 7.0.0}
    next(reader) #{CSV separator: Semicolon}
    line = next(reader) #{Decimal separator: .}
    system_meta_info['decimal_separator'] = line[0][-2:-1]
    next(reader) #{Date separator: /}
    next(reader) #{Short date format: M/d/yyyy}
    
    return system_meta_info
