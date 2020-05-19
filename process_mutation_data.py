import pandas as pd
import numpy as np

file_path = '12-output.xml.out'
with open(file_path) as infile:
    list_of_col_name = ['nucid', 'nuc_name']
    for i in range(1, 22):
        list_of_col_name.append(str(i))

    print(list_of_col_name)
    print(len(list_of_col_name))
    read_file = pd.read_csv(filepath_or_buffer=file_path, engine='python',
                            sep='\\s+', skiprows=1, skipfooter=3, names=list_of_col_name)
    print(read_file)
