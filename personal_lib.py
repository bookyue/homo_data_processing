import glob
import json
import os
import re
from collections import deque

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def group_compare(method_run, out_dir):
    df_add = deque()
    file_names = glob.glob('./*.csv')
    file_names = sorted(file_names)

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

            is_tta_null = method_run(file_names[i], file_names[j], passed_list, is_gamma)[1]
            if is_tta_null:
                tmp_add = method_run(file_names[i+1], file_names[j], passed_list, is_gamma)[0]
            else:
                tmp_add = method_run(file_names[i], file_names[j], passed_list, is_gamma)[0]

            df_add.append(tmp_add)
            # print(df_add.pop())
        if is_gamma:
            df_result = df_add.popleft()
            df_result.columns = ['Energy', 'TTA', 'CRAM']

            tmp_pop = df_add.popleft()
            tmp_pop.columns = ['Energy', 'TTA', 'QRAM']
            df_result = pd.merge(df_result, tmp_pop, how='outer', on=['Energy', 'TTA'])

            tmp_pop = df_add.popleft()
            tmp_pop.columns = ['Energy', 'TTA', 'LPAM']
            df_result = pd.merge(df_result, tmp_pop, how='outer', on=['Energy', 'TTA'])

            tmp_pop = df_add.popleft()
            tmp_pop.columns = ['Energy', 'TTA', 'MMPA']
            df_result = pd.merge(df_result, tmp_pop, how='outer', on=['Energy', 'TTA'])

            df_result = df_result[['Energy', 'TTA', 'CRAM', 'QRAM', 'LPAM', 'MMPA']]

        else:
            df_result = df_add.popleft()
            df_result.columns = ['nucid', 'nuc_name', 'TTA', 'CRAM']

            tmp_pop = df_add.popleft()
            tmp_pop.columns = ['nucid', 'nuc_name', 'TTA', 'QRAM']
            df_result = pd.merge(df_result, tmp_pop, how='outer', on=['nucid', 'nuc_name', 'TTA'])

            tmp_pop = df_add.popleft()
            tmp_pop.columns = ['nucid', 'nuc_name', 'TTA', 'LPAM']
            df_result = pd.merge(df_result, tmp_pop, how='outer', on=['nucid', 'nuc_name', 'TTA'])

            tmp_pop = df_add.popleft()
            tmp_pop.columns = ['nucid', 'nuc_name', 'TTA', 'MMPA']
            df_result = pd.merge(df_result, tmp_pop, how='outer', on=['nucid', 'nuc_name', 'TTA'])

            # correct columns order
            df_result = df_result[['nucid', 'nuc_name', 'TTA', 'CRAM', 'QRAM', 'LPAM', 'MMPA']]

            df_result.sort_values(by='nucid', inplace=True)
        
        if is_tta_null:
            df_result['TTA'], df_result['CRAM'] = df_result['CRAM'].copy(), df_result['TTA'].copy()
        print(df_result)
        out_name = f'{front_base_file_name}{str((i * 6) + 1).zfill(3)}-' \
                   f'{str((i + 5) * 6).zfill(3)}-{end_base_file_name}.csv'

        # out_dir = './result'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        fullname = os.path.join(out_dir, out_name)

        df_result.to_csv(fullname, index=False)

        i += 5

        if i == len(file_names):
            break
