import os
import re
import pandas as pd
import numpy as np
import glob
from collections import deque


def method_compare(in_file1, in_file2, is_gamma):
    df1 = pd.read_csv(in_file1, dtype={'Energy': str})
    df2 = pd.read_csv(in_file2, dtype={'Energy': str})

    if is_gamma:
        df_merged = pd.merge(df1, df2, how='outer', on=['Energy'])
        df_merged.replace(to_replace=[np.inf, -np.inf], value=np.nan, inplace=True)
    else:
        df_merged = pd.merge(df1, df2, how='outer', on=['nucid', 'nuc_name'])
        df_merged.replace(to_replace=[np.inf, -np.inf], value=np.nan, inplace=True)
        nuclide_list = ['Np237', 'Pa233', 'U233', 'Th229', 'Ra225', 'Ac225', 'Fr221', 'At217', 'Bi213', 'Po213',
                        'Tl209', 'Pb209', 'Bi209', 'U234', 'U235', 'U236', 'U238', 'U239', 'Np237', 'Np239', 'Pu238',
                        'Pu239', 'Pu240', 'Pu241', 'Pu242', 'Am241', 'Am242', 'Am243', 'Cm242', 'Cm244', 'H3', 'Mo95',
                        'Tc99', 'Ru103', 'Ag109', 'Xe135', 'Cs133', 'Nd143', 'Nd145', 'Sm147', 'Sm149', 'Sm150',
                        'Sm151', 'Sm152', 'Eu153', 'Gd155']

    print(df_merged)

    # relative tolerance
    # abs(X - Y) / 1 + min(abs(X), abs(Y))
    relative_numeric_tolerance_e_5 = (np.abs(df_merged.iloc[:, -2] - df_merged.iloc[:, -1]) / (
            1 + np.where(np.abs(df_merged.iloc[:, -2]) < np.abs(df_merged.iloc[:, -1]), np.abs(df_merged.iloc[:, -2]),
                         np.abs(df_merged.iloc[:, -1])))) > 1e-5

    is_not_the_same = df_merged.iloc[:, -2] != df_merged.iloc[:, -1]
    is_too_small_number_x = np.abs(df_merged.iloc[:, -2]) > 1e-30
    is_too_small_number_y = np.abs(df_merged.iloc[:, -1]) > 1e-30

    df_output = pd.DataFrame(df_merged[is_not_the_same & relative_numeric_tolerance_e_5 &
                                       is_too_small_number_x & is_too_small_number_y])
    if not is_gamma:
        df_output = df_output[df_output['nuc_name'].isin(nuclide_list)]
    return df_output


def group_compare():
    df_add = deque()
    file_names = glob.glob('./*.csv')

    pattern = re.compile('^\./(\D+)\d+-\d+-(\w+)\.csv$')
    front_base_file_name = pattern.match(file_names[0]).group(1)
    end_base_file_name = pattern.match(file_names[0]).group(2)

    if 'gamma' == end_base_file_name:
        is_gamma = True
    else:
        is_gamma = False

    i = 0
    while True:
        for j in range(i + 1, i + 5):
            df_add.append(method_compare(file_names[i], file_names[j], is_gamma))
            # print(df_add.pop())
        if is_gamma:
            df_result = df_add.popleft()
            df_result.columns = ['Energy', 'TTA', 'CRAM']

            tmp = df_add.popleft()
            tmp.columns = ['Energy', 'TTA', 'QRAM']
            df_result = pd.merge(df_result, tmp, how='outer', on=['Energy', 'TTA'])

            tmp = df_add.popleft()
            tmp.columns = ['Energy', 'TTA', 'LPAM']
            df_result = pd.merge(df_result, tmp, how='outer', on=['Energy', 'TTA'])

            tmp = df_add.popleft()
            tmp.columns = ['Energy', 'TTA', 'MMPA']
            df_result = pd.merge(df_result, tmp, how='outer', on=['Energy', 'TTA'])

            df_result = df_result[['Energy', 'TTA', 'CRAM', 'QRAM', 'LPAM', 'MMPA']]

        else:
            df_result = df_add.popleft()
            df_result.columns = ['nucid', 'nuc_name', 'TTA', 'CRAM']

            tmp = df_add.popleft()
            tmp.columns = ['nucid', 'nuc_name', 'TTA', 'QRAM']
            df_result = pd.merge(df_result, tmp, how='outer', on=['nucid', 'nuc_name', 'TTA'])

            tmp = df_add.popleft()
            tmp.columns = ['nucid', 'nuc_name', 'TTA', 'LPAM']
            df_result = pd.merge(df_result, tmp, how='outer', on=['nucid', 'nuc_name', 'TTA'])

            tmp = df_add.popleft()
            tmp.columns = ['nucid', 'nuc_name', 'TTA', 'MMPA']
            df_result = pd.merge(df_result, tmp, how='outer', on=['nucid', 'nuc_name', 'TTA'])

            # correct columns order
            df_result = df_result[['nucid', 'nuc_name', 'TTA', 'CRAM', 'QRAM', 'LPAM', 'MMPA']]

            df_result.sort_values(by='nucid', inplace=True)

        print(df_result)
        out_name = f'{front_base_file_name}{str((i * 6) + 1).zfill(3)}-' \
                  f'{str((i + 5) * 6).zfill(3)}-{end_base_file_name}.csv'

        out_dir = './result'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        fullname = os.path.join(out_dir, out_name)

        df_result.to_csv(fullname, index=0)

        i += 5

        if i == len(file_names):
            break


def main():
    group_compare()


main()
