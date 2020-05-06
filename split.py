import re
import glob
from pathlib import Path
import shutil


def split_xml_out_file(file_name, line_numbers_of_results):
    with open(file_name) as unprocessed_file:
        lines = unprocessed_file.readlines()
        # export file name
        # *.xml.out -> *.extension.out
        pattern = re.compile("^(.*)\.xml\.out$")
        base_file_name =  pattern.match(file_name).group(1)

        target_file_names = []
        target_extensions = ["density", "radioactivity", "absorption", "fission", "heat", "gamma"]
        for extension in target_extensions:
            target_file_names.append(base_file_name+"-"+extension+".out")
        # print(target_file_names)

        target_files = []
        for target_file_name in target_file_names:
            target_files.append(open(target_file_name, "w+"))
        # print(target_files)
        
        for i, target_file in enumerate(target_files):
            target_file.writelines(lines[line_numbers_of_results[2*i]:line_numbers_of_results[2*i+1]+1])

        for target_file in target_files:
            target_file.close()

    return


def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_numbers_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line_number, line in enumerate(read_obj):
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    line_numbers_of_results.append(line_number)
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return line_numbers_of_results



def organize_files():
    file_names = glob.glob("./*.out")

    list_directories = ["absorption", "density", "fission", "gamma", "heat", "radioactivity"]
    
    if file_names:
        for directory_name in list_directories:
            Path(directory_name).mkdir(exist_ok=True)

        for file_name in file_names:
            for directory_name in list_directories:
                if directory_name in file_name:
                    shutil.move(file_name, directory_name)
    else:
        print("No *.out files")
    return


def main():

    # search for given strings in files
    # and return list of tuples containing line numbers
    list_of_strings = ["NucID", "Total", "Energy"]

    files_name = glob.glob("./*.xml.out")
    for file_name in files_name:
        print(file_name)
        matched_lines = search_multiple_strings_in_file(file_name, list_of_strings)
        
        if not matched_lines:
            split_xml_out_file(file_name, matched_lines)
        else:
            print(f"Warning!!! {file_name} dosen't contain searched strings")
    
    organize_files()


main()