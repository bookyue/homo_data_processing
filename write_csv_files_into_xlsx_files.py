import glob
import os
import re
from collections import defaultdict
import pandas as pd


def scan_csv_files():
    file_names = glob.glob('./*.csv')

    pattern = re.compile('^\./(\D+)(\d+)-\d+-(\w+)\.csv$')
    front_base_file_name = pattern.match(file_names[0]).group(1)
    i = 0
    j = 0
    out_names = []

    while True:
        out_names.append(f'{front_base_file_name}{str((i * 6) + 1).zfill(3)}-{str((i + 5) * 6).zfill(3)}.xlsx')
        i += 5
        j += 1
        if j >= len(file_names) / 6:
            break

    flag_file_name_num = []
    flag_file_name_str = []
    for file_name in file_names:
        flag_file_name_num.append(pattern.match(file_name).group(2))
        flag_file_name_str.append(pattern.match(file_name).group(3))
    flag_file_name_num = list(dict.fromkeys(flag_file_name_num))
    flag_file_name_str = list(dict.fromkeys(flag_file_name_str))
    # print(flag_file_name_num)
    # print(flag_file_name_str)

    file_list = defaultdict(list)
    for flag_num in flag_file_name_num:
        for file_name in file_names:
            if flag_num in file_name:
                file_list[flag_num].append(file_name)

    return file_list, flag_file_name_str, out_names


def merge_csv_files_into_xlsx_files(file_names, out_name, sheet_names):
    writer = pd.ExcelWriter(out_name)
    for csv_file_name, sheet_name in zip(file_names, sheet_names):
        df = pd.read_csv(csv_file_name, dtype={0: str})
        df.to_excel(writer, sheet_name=os.path.splitext(sheet_name)[0], index=False, engine='openpyxl')
    writer.save()


def main():
    file_list, flag_file_name_str, out_names = scan_csv_files()
    # print(file_list)
    # print(flag_file_name_str)
    # print(out_names)
    i = 0
    for flag_file_name_num, file_names in file_list.items():
        merge_csv_files_into_xlsx_files(file_names, out_names[i], flag_file_name_str)
        i += 1


main()
