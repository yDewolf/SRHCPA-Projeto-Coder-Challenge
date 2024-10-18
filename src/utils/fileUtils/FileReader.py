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
    pass

# Custom stringifying function to properly format values to string
def stringify_value(value):
    pass