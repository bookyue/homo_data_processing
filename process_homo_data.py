import sys

import numpy as np
import pandas as pd

from personal_lib import group_compare


def method_compare(in_file1: pd.DataFrame, in_file2: pd.DataFrame, nuclide_list: list, is_gamma: bool) -> pd.DataFrame:
    """
    Args:
        in_file1: filepath_or_bufferstr, path object or file-like object
        in_file2: filepath_or_bufferstr, path object or file-like object
        nuclide_list: a list of nuclide
        is_gamma: if handling gamma files is True, and vice versa
        is_process: turn on or off the process switch

    Returns:
        df_output: a DataFrame object
    """
    header_list = ['Energy', 'nucid', 'nuc_name']
    if is_gamma:
        df1 = pd.read_csv(in_file1, dtype={'Energy': str})
        df2 = pd.read_csv(in_file2, dtype={'Energy': str})
        header_list = header_list[0:1]
    else:
        df1 = pd.read_csv(in_file1)
        df2 = pd.read_csv(in_file2)
        df1 = df1[df1['nuc_name'].isin(nuclide_list)]
        df2 = df2[df2['nuc_name'].isin(nuclide_list)]
        header_list = header_list[1:3]

    df_merged = pd.merge(df1, df2, how='outer', on=header_list)

    if not is_gamma:
        df_merged = df_merged[['nucid', 'nuc_name', 'result_x', 'result_y']]
    else:
        df_merged = df_merged[['Energy', 'result_x', 'result_y']]

    df_merged.replace(to_replace=[np.inf, -np.inf], value=np.nan, inplace=True)

    is_tta_null = df1.isnull().all().all()

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

    return df_output, is_tta_null


def main():
    group_compare(method_compare, sys.argv[1])


main()
