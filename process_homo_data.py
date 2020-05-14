import numpy as np
import pandas as pd

from personal_lib import group_compare


def method_compare(in_file1, in_file2, is_gamma):
    """
    Args:
        in_file1: filepath_or_bufferstr, path object or file-like object
        in_file2: filepath_or_bufferstr, path object or file-like object
        is_gamma: if handling gamma files is True, and vice versa
    """
    if is_gamma:
        df1 = pd.read_csv(in_file1, dtype={'Energy': str})
        df2 = pd.read_csv(in_file2, dtype={'Energy': str})
        df_merged = pd.merge(df1, df2, how='outer', on=['Energy'])
        df_merged.replace(to_replace=[np.inf, -np.inf], value=np.nan, inplace=True)
    else:
        df1 = pd.read_csv(in_file1)
        df2 = pd.read_csv(in_file2)
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


def main():
    group_compare(method_compare)


main()
