import glob


def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1

            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))

    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results


def main():
    files_name = glob.glob('./*.xml.out')
    matched_lines = []
    list_of_strings = ['-NAN(IND)']

    for file_name in files_name:
        print(file_name)
        matched_lines = search_multiple_strings_in_file(file_name, list_of_strings)

    print('Total Matched lines : ', len(matched_lines))
    for elem in matched_lines:
        print('Word = ', elem[0], ' :: Line Number = ', elem[1], ' :: Line = ', elem[2])


main()
