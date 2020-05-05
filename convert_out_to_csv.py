import pandas as pd
import re
import glob


# convert out file to csv file
def out_to_csv(file_name):
    read_file = pd.read_fwf(file_name)
    out_csv_file = pd.DataFrame(read_file, columns=["NucID", "nuc_name", "Unnamed: 3"])
    out_csv_file.rename(columns={"Unnamed: 3": "result"}, inplace=True)

    pattern = re.compile("^(.*)\.out$")
    base_file_name =  pattern.match(file_name).group(1)
    out_file_name = base_file_name + ".csv"

    out_csv_file.to_csv(out_file_name, index=0)


def main():
    file_names = glob.glob("./*.out")
    for file_name in file_names:
        print(file_name)
        out_to_csv(file_name)


main()