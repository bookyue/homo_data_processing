import pandas as pd
import numpy as np
import glob
from collections import deque

def method_compare(in_file1, in_file2):
    df1 = pd.read_csv(in_file1)
    df2 = pd.read_csv(in_file2)

    df_merged = pd.merge(df1, df2, how="outer", on=["nucid", "nuc_name"])
    df_merged.replace(to_replace=[np.inf, -np.inf], value=np.nan, inplace=True)
    print(df_merged)

    # relative tolerance
    # abs(X - Y) / 1 + min(abs(X), abs(Y))
    is_less_than_e_9 = (np.abs(df_merged.iloc[:, 2]-df_merged.iloc[:, 3]) / 1 + np.where(np.abs(df_merged.iloc[:, 2]) < np.abs(df_merged.iloc[:, 3]), np.abs(df_merged.iloc[:, 2]), np.abs(df_merged.iloc[:, 3]))) < 1e-9
    is_greater_than_e_9 = (np.abs(df_merged.iloc[:, 2]-df_merged.iloc[:, 3]) / 1 + np.where(np.abs(df_merged.iloc[:, 2]) < np.abs(df_merged.iloc[:, 3]), np.abs(df_merged.iloc[:, 2]), np.abs(df_merged.iloc[:, 3]))) > 1e-9

    is_not_the_same = df_merged.iloc[:, 2] != df_merged.iloc[:, 3]
    is_too_small_number_x = np.abs(df_merged.iloc[:, 2]) > 1e-26
    is_too_small_number_y = np.abs(df_merged.iloc[:, 3]) > 1e-26
    
    df_output = pd.DataFrame(df_merged[is_not_the_same & is_too_small_number_x & is_too_small_number_y & (is_less_than_e_9 | is_greater_than_e_9)])

    return df_output


def group_compare():
    df_add = deque()
    file_names = glob.glob("./*.csv")
    i = 0
    j = 0
    while True:
        for j in range(i+1, i+5):
            df_add.append(method_compare(file_names[i], file_names[j]))
            # print(df_add.pop())
        df_result = df_add.popleft()
        df_result.columns = ["nucid", "nuc_name", "TTA", "CRAM"]
        
        tmp = df_add.popleft()
        tmp.columns = ["nucid", "nuc_name", "TTA", "QRAM"]
        df_result = pd.merge(df_result, tmp, how="outer", on=["nucid", "nuc_name", "TTA"])
        
        tmp = df_add.popleft()
        tmp.columns = ["nucid", "nuc_name", "TTA", "LPAM"]
        df_result = pd.merge(df_result, tmp, how="outer", on=["nucid", "nuc_name", "TTA"])
        
        tmp = df_add.popleft()
        tmp.columns = ["nucid", "nuc_name", "TTA", "MMPA"]
        df_result = pd.merge(df_result, tmp, how="outer", on=["nucid", "nuc_name", "TTA"])
        
        # correct colums order
        df_result = df_result[["nucid", "nuc_name", "TTA", "CRAM", "QRAM", "LPAM", "MMPA"]]
        
        df_result.sort_values(by='nucid', inplace=True)
        print(df_result)
        df_result.to_csv("结果" + str(i*6) + ".csv", index=0)
        i += 5

        if i == len(file_names):
            break


def main():
    group_compare()

main()
