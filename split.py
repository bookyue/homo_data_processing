import re
import glob

def split_xml_out_file(file_name, line_numbers_of_results):
    with open(file_name) as unprocessed_file:
        lines = unprocessed_file.readlines()
        # export file name
        # *.xml.out -> *.extension.out
        pattern = re.compile("^(.*)\.xml\.out$")
        base_file_name =  pattern.match(file_name).group(1)
        density_extension = base_file_name + "-density.out"
        radioactivity_extension = base_file_name + "-radioactivity.out"
        absorption_rate_extension = base_file_name + "-absorption.out"
        fission_extension = base_file_name + "-fission.out"
        heat_extension = base_file_name + "-heat.out"
        gamma_extension = base_file_name + "-gamma.out"

        for i, line in enumerate(lines):
            # split and wrtie density data into file
            if i >= line_numbers_of_results[0] and i <= line_numbers_of_results[1]:
                density_data = open(density_extension, "a+")
                density_data.writelines(line)

            # split and write radioactivity data into file
            elif i >= line_numbers_of_results[2] and i <= line_numbers_of_results[3]:
                radioactivity_data = open(radioactivity_extension, "a+")
                radioactivity_data.writelines(line)

            # split and write absorption rate data into file
            elif i >= line_numbers_of_results[4] and i <= line_numbers_of_results[5]:
                absorption_rate_data = open(absorption_rate_extension, "a+")
                absorption_rate_data.writelines(line)
            
            # split and write fission data into file
            elif i >= line_numbers_of_results[6] and i <= line_numbers_of_results[7]:
                fission_data = open(fission_extension, "a+")
                fission_data.writelines(line)
            
            # split and write heat data into file
            elif i >= line_numbers_of_results[8] and i <= line_numbers_of_results[9]:
                heat_data = open(heat_extension, "a+")
                heat_data.writelines(line)

            # split and write gamma data into file
            elif i >= line_numbers_of_results[10] and i <= line_numbers_of_results[11]:
                gamma_data = open(gamma_extension, "a+")
                gamma_data.writelines(line)
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


def main():

    # search for given strings in files
    # and return list of tuples containing line numbers
    list_of_strings = ["NucID", "Total", "Energy"]

    files_name = glob.glob("./*.xml.out")
    for file_name in files_name:
        print(file_name)
        matched_lines = search_multiple_strings_in_file(file_name, list_of_strings)
        split_xml_out_file(file_name, matched_lines)


main()