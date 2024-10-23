# General file reading
import os as OS

def create_file(file_path: str, store_string: str = ""):
    with open(file_path, "x") as file:
        file.write(store_string)

def save_file(file_path: str, data_as_str: str = "", overwrite: bool = True, auto_create: bool = True):
    if overwrite:
        if not OS.path.exists(file_path):
            create_file(file_path, data_as_str)
            return

        with open(file_path, "w") as file:
            file.write(data_as_str)
        
        return
    
    with open(file_path, "a") as file:
        file.write(data_as_str)


def get_file_lines(file_path: str) -> list:
    lines = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            lines.append(line.replace("\n", ""))
    
    return lines

# Custom parsing function to properly assign types from strings
def parse_string_value(value: str):
    # If value is enclosed by ''
    print(value)
    if value.__contains__("'"):
    #if value.startswith("'") and value.endswith("'"):
        # Return the same value but without the ''
        return value.replace("'", "").replace(";", ",")

    # If value is enclosed by []
    if value.startswith("[") and value.endswith("]"):
        value_list = []
        value = value.replace("[", "").replace("]", "")
        for val in value.split(";"):
            value_list.append(parse_string_value(val))
        
        return value_list

    if value.__contains__("."):
        return float(value)
    
    return int(value)

# Custom stringifying function to properly format values to string
def stringify_value(value, inside_list: bool = False):
    if type(value) is list:
        stringified_list = []
        for val in value:
            stringified_list.append(stringify_value(val, True))
        
        list_str = str(stringified_list)
        list_str = list_str.replace(",", ";")
        return list_str
    
    if type(value) is str:
        return ("'" + value + "'").replace(",", ";")

    if inside_list:
        return value
    
    return str(value)
