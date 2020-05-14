import pandas as pd
import re
import glob
from pathlib import Path
import shutil


# convert out file to csv file
def out_to_csv(file_name, is_gamma=False):
    if is_gamma:
        read_file = pd.read_csv(file_name, sep='\s+', skiprows=1, skipfooter=2, engine='python',
                                names=['Energy', 'remove', 'result'], dtype={'Energy': str})
        out_csv_file = pd.DataFrame(read_file, columns=['Energy', 'result'])
    else:
        read_file = pd.read_csv(file_name, sep='\s+', skiprows=1, skipfooter=3, engine='python',
                                names=['nucid', 'nuc_name', 'remove', 'result'])
        out_csv_file = pd.DataFrame(read_file, columns=['nucid', 'nuc_name', 'result'])

    pattern = re.compile('^(.*)\\.out$')
    base_file_name = pattern.match(file_name).group(1)
    out_file_name = base_file_name + '.csv'

    out_csv_file.to_csv(out_file_name, index=False)


def organize_files():
    Path('./csv').mkdir(exist_ok=True)

    file_names = glob.glob('./*.csv')
    for file_name in file_names:
        shutil.move(file_name, './csv')
    return


def main():
    file_names = glob.glob('./*.out')
    for file_name in file_names:
        print(file_name)
        if 'gamma' in file_name:
            out_to_csv(file_name, True)
        else:
            out_to_csv(file_name)

    organize_files()


main()
