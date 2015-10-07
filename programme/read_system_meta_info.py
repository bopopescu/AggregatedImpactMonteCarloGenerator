def read_system_meta_info(reader):
    
    #the first few lines of the file are not very useful.  
    #only fetching the project name and decimal separator
    system_meta_info = {}
    next(reader) #{SimaPro 7.3} or {SimaPro 8.*}
    next(reader) #{processes}
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
