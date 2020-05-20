import sys
from typing import Tuple

import pandas as pd

from personal_lib import group_compare


def merger(in_file1: pd.DataFrame, in_file2: pd.DataFrame, nuclide_list: list, is_gamma: bool) -> Tuple[pd.DataFrame, bool]:
    """
    Args:
        nuclide_list: a list of nuclide
        in_file1: filepath_or_bufferstr, path object or file-like object
        in_file2: filepath_or_bufferstr, path object or file-like object
        is_gamma: if handling gamma files is True, and vice versa

    Returns:
        df_merged: a DataFrame object
        False: TTA is not NULL
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

    return df_merged, False


def main():
    group_compare(merger, sys.argv[1])


main()
