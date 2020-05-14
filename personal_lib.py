from array import array
import glob
import json
import os
import re
from collections import deque

import pandas as pd


def group_compare(method_run):
    df_add = deque()
    file_names = glob.glob('./*.csv')

    nuclid_list = json.loads(os.getenv('NUCLID_LIST'))
    pure_decay_list = list(map(int, json.loads(os.getenv('PURE_DECAY_SPLIT'))))
    print(type(pure_decay_list))

    pattern = re.compile('^\./(\D+)(\d+)-\d+-(\w+)\.csv$')
    front_base_file_name = pattern.match(file_names[0]).group(1)
    end_base_file_name = pattern.match(file_names[0]).group(3)

    if 'gamma' == end_base_file_name:
        is_gamma = True
    else:
        is_gamma = False

    i = 0
    while True:
        for j in range(i + 1, i + 5):
            order_num = int(pattern.match(file_names[i]).group(2))
            if pure_decay_list[1] >= order_num >= pure_decay_list[0]:
                passed_list = nuclid_list['decay']
            elif pure_decay_list[2] <= order_num <= pure_decay_list[3]:
                passed_list = nuclid_list['decay']
            else:
                passed_list = nuclid_list['flux']

            df_add.append(method_run(file_names[i], file_names[j], passed_list, is_gamma))
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

        df_result.to_csv(fullname, index=False)

        i += 5

        if i == len(file_names):
            break
