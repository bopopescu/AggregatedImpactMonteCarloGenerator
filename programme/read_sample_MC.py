def read_sample_MC(filename):
    import csv
    reader = csv.reader(open(filename,'U'), delimiter=';')
    
    cell_ID = 0
    sample = []
    while 1:
        cell_ID += 1
        try:
            sample[cell_ID] = next(reader)
        except StopIteration:
            break
    
    return sample