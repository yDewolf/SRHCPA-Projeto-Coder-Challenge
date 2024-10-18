# CSV file reader
import FileReader


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
            line_dict[headerKey] = splitted_line[column_idx]
        
        csv_rows.append(line_dict)
    
    return csv_rows


def get_csv_values_with_key(file_path: str, header: list[str] = [], main_key: str = "", separator: str = ",") -> dict:
    raw_values = get_csv_rows(file_path, header, separator)
    if main_key == "":
        main_key = header[0]

    indexed_csv = {}

    for row_dict in raw_values:
        filtered_dict = {}

        for key in row_dict:
            # Skip main key
            if key == main_key:
                continue
            
            filtered_dict[key] = row_dict[key]

        # Index the value from row_dict that corresponds to the main key column as the filtered_dict
        indexed_csv[row_dict[main_key]] = filtered_dict

    return indexed_csv
