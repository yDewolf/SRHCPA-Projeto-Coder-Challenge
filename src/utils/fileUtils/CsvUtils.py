# CSV file reader
import os
import utils.fileUtils.FileUtils as FileUtils
#import FileUtils

# Function for saving a dictionary (that has other dictionaries in it) as a csv file
def save_dict_as_csv(file_path: str, dictionary: dict, main_key: str, header: list[str], overwrite: bool = False):
    if not os.path.isfile(file_path):
        # Push warning
        print(f"WARNING: Provided path doesn't lead to a file, a new file will be created | path: {file_path}")

    csv_lines = ""
    # Create a header line if the file will be overwritten
    header_line = _get_header_line(file_path, header)
    header = header_line.split(",")

    if overwrite:
        csv_lines += header_line + "\n"

    for idx, main_key_value in enumerate(dictionary):
        # Add main key back to the filtered dictionary
        dictionary[main_key_value][main_key] = main_key_value

        if not type(dictionary[main_key_value]) is dict:
            # Push error:
            print(f"ERROR: Invalid dictionary structure in save_dict_as_csv | Dictionary: {dictionary}")
            return False

        # Create csv line from dictionary
        csv_line = dict_to_csv(dictionary[main_key_value], header)

        # Add the line of this dictionary to csv file lines
        csv_lines += csv_line
        if idx < len(dictionary) - 1:
            csv_lines += "\n"
    
    FileUtils.save_file(file_path, csv_lines, overwrite)
    return csv_lines

def save_rows_as_csv(file_path: str, rows_list: list[dict], header: list[str], overwrite: bool = False):
    if not os.path.isfile(file_path):
        # Push warning
        print(f"WARNING: Provided path doesn't lead to a file, a new file will be created | path: {file_path}")
        #return

    csv_lines = ""
    header_line = _get_header_line(file_path, header)
    header = header_line.split(",")
        
    # Add header if the file will be overwritten
    if overwrite:
        csv_lines += header_line
    
    csv_lines += "\n"

    for idx, row_dict in enumerate(rows_list):
        csv_lines += dict_to_csv(row_dict, header)
        if idx < len(rows_list) - 1:
            csv_lines += "\n"
    
    FileUtils.save_file(file_path, csv_lines, overwrite)
    return csv_lines


def get_csv_rows(file_path: str, header: list[str] = [], separator: str = ",") -> list[dict]:
    file_lines = FileUtils.get_file_lines(file_path)
    
    # Get header from file if a header wasn't inputted
    full_header = _get_header_line(file_path).split(separator)
    if header == []:
        header = full_header

    csv_rows = []

    for line in file_lines:
        # Skip header line
        if line == file_lines[0]:
            continue
        
        splitted_line = line.split(separator)

        line_dict = {}
        for column_idx, headerKey in enumerate(full_header):
            if not header.__contains__(headerKey):
                continue
            # Header key = respective value in this line
            line_dict[headerKey] = FileUtils.parse_string_value(splitted_line[column_idx])
        
        csv_rows.append(line_dict)
    
    return csv_rows

def get_csv_values_with_key(file_path: str, header: list[str] = [], main_key: str = "", separator: str = ",") -> dict:
    raw_values = get_csv_rows(file_path, header, separator)
    if main_key == "" and len(header) != 0:
        main_key = header[0]

    indexed_csv = {}

    for row_dict in raw_values:
        main_key_value = row_dict[main_key]
        row_dict.pop(main_key)
        filtered_dict = row_dict
        
        # Index value from row_dict that corresponds to the main key column as the filtered_dict
        indexed_csv[main_key_value] = filtered_dict

    return indexed_csv


# Create a csv line with the given dictionary values
def dict_to_csv(dictionary: dict, header: list[str]) -> str:
    csv_str = ""
    for idx, header_key in enumerate(header):
        value_str = FileUtils.stringify_value(dictionary[header_key])
        csv_str += value_str

        if idx < len(header) - 1:
            csv_str += ","
    
    return csv_str

# Returns a header str from the existing file or from the provided header as list
def _get_header_line(file_path: str, header: list[str] = []) -> str:
    header_line = ""
    if len(header) == 0 and os.path.isfile(file_path):
        # Get an existing header line
        with open(file_path, "r") as file:
            header_line = file.readline()
            file.close()
        
        return header_line.replace("\n", "")
    
    # Create header line from provided header
    for idx, key in enumerate(header):
        header_line += key

        if idx < len(header) - 1:
            header_line += ","
    
    return header_line


# Scuffed way of showing csv files
def get_formatted_csv(file_path: str, header: list[str] = []):
    header = _get_header_line(file_path, header).split(",")
    csv_rows = get_csv_rows(file_path, header)

    table_str = ""

    # (Columns by Rows or y, x)
    table_matrix = [
    ]
    for row in range(len(csv_rows) + 1):
        table_matrix.append([])

    # Get max widths
    max_widths = []
    for idx, header_key in enumerate(header):
        max_widths.append(len(header_key))

        for row_dict in csv_rows:
            if max_widths[idx] < len(str(row_dict[header_key])):
                max_widths[idx] = len(str(row_dict[header_key]))


    for header_key_idx, header_key in enumerate(header):
        max_width = max_widths[header_key_idx]
        header_composition = []
        top_str = f"+{"-"* (max_width + 2)}"
        if header_key_idx == len(header) - 1:
            top_str += "+"

        mid_str = f"| {header_key.rjust(max_width)} "
        if header_key_idx == len(header) - 1:
            mid_str += "|"

        header_composition.append(top_str)
        header_composition.append(mid_str)

        table_matrix[0].append(header_composition)

        for row_idx in range(len(csv_rows)):
            row_composition = []

            top_str = f"+{"-"* (max_width + 2)}"
            mid_str = f"| {str(csv_rows[row_idx][header_key]).rjust(max_width)} "
            bottom_str = f""
            if row_idx == len(csv_rows) - 1:
                bottom_str = f"+{"-"* (max_width + 2)}"

                if header_key_idx == len(header) - 1:
                    bottom_str += "+"

            if header_key_idx == len(header) - 1:
                top_str += "+"
                mid_str += "|"

            row_composition.append(top_str)
            row_composition.append(mid_str)
            row_composition.append(bottom_str)

            table_matrix[row_idx + 1].append(row_composition)

    header_str = ""
    for row_idx in range(len(table_matrix)):
        for composition_row_idx in range(len(table_matrix[row_idx][0])):
            composition_row_str = ""

            for composition_idx in range(len(table_matrix[row_idx])):
                composition_row_str += table_matrix[row_idx][composition_idx][composition_row_idx]

            if composition_row_str != "":
                header_str += composition_row_str + "\n"

    table_str += header_str

    return table_str

#csv_dict = get_csv_values_with_key("data/users.csv", main_key="id")
#save_dict_as_csv("data/users1.csv", csv_dict, "id", ["id", "login", "password", "permission_level"], True)
#csv_rows = get_csv_rows("data/users.csv")
#save_rows_as_csv("data/users.csv", csv_rows, [])