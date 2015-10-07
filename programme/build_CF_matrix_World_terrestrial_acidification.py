def build_CF_matrix_World_terrestrial_acidification(CF, EF_list):
    from scipy.sparse import lil_matrix
    country = CF.keys()[0]
    
    print 'building matrices for IW terrestrial_acidification per country'
    print ''
    mid_end = CF[country].keys()[0]
    substance_columns = {}
    for substance in CF[country][mid_end]:
        substance_columns[substance] = []
        for column_number in range(len(EF_list)):
            EF = EF_list[column_number]
            if EF[0] == 'Air' and EF[1] == substance:
                substance_columns[substance].append(column_number)
    print substance_columns
    for country in CF:
        CF_matrices['IW ter. acid. ' + country] = lil_matrix((2, len(EF_list)))
        for mid_end in CF[country]:
            if mid_end == 'midpoint':
                line_number = 0
            else:
                line_number = 1
            for substance in CF[country][mid_end]:
                for column_number in substance_columns[substance]:
                    CF_matrices['IW ter. acid. ' + country][line_number, column_number] = CF[country][mid_end][substance]
    
    return CF_matrices
