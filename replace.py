import glob
import re
import shutil
from pathlib import Path


def replace_strings(file_name, replaced_string, replace_string):
    pattern = re.compile('^(.*)\.xml\.out$')
    base_file_name = pattern.match(file_name).group(1)

    in_file_name = base_file_name + '.xml.out.broken'
    out_file_name = base_file_name + '.xml.out'

    shutil.move(file_name, in_file_name)

    with open(in_file_name, 'rt') as fin:
        with open(out_file_name, 'wt') as fout:
            for line in fin:
                fout.write(line.replace(replaced_string, replace_string))


def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    is_appear = False
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # print(line)
                    is_appear = True
    return is_appear


def organize_files():
    file_names = glob.glob('./*.broken')

    if file_names:
        Path('broken').mkdir(exist_ok=True)

        for file_name in file_names:
            shutil.move(file_name, 'broken')
    else:
        print('No *.broken files')
    return


def main():
    file_names = glob.glob('./*.xml.out')
    list_of_strings = ['-NAN(IND)', 'NAN']
    for file_name in file_names:
        if search_multiple_strings_in_file(file_name, list_of_strings):
            replace_strings(file_name, '-NAN(IND)', '-INF')
            replace_strings(file_name, 'NAN', 'NaN')
    organize_files()


main()
