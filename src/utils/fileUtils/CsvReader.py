# CSV file reader
import os
import FileReader

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
    
    FileReader.save_file(file_path, csv_lines, overwrite)
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
    
    FileReader.save_file(file_path, csv_lines, overwrite)
    return csv_lines


def get_csv_rows(file_path: str, header: list[str] = [], separator: str = ",") -> list[dict]:
    file_lines = FileReader.get_file_lines(file_path)
    
    # Get header from file if a header wasn't inputted
    if len(header) == 0:
        # Header should be the first line of the file
        header = file_lines[0].split(separator)

    csv_rows = []

    for line in file_lines:
        # Skip header line
        if line == file_lines[0]:
            continue
        
        splitted_line = line.split(separator)

        line_dict = {}
        for column_idx, headerKey in enumerate(header):
            # Header key = respective value in this line
            line_dict[headerKey] = FileReader.parse_string_value(splitted_line[column_idx])
        
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
        value_str = FileReader.stringify_value(dictionary[header_key])
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


#csv_dict = get_csv_values_with_key("data/users.csv", main_key="id")
#save_dict_as_csv("data/users1.csv", csv_dict, "id", ["id", "login", "password", "permission_level"], True)
#csv_rows = get_csv_rows("data/users.csv")
#save_rows_as_csv("data/users.csv", csv_rows, [])