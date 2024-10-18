# Ship registration utils
import fileUtils.FileReader as FileReader
from fileUtils.CsvReader import dict_to_csv
from Ship import Ship

parameters = {}

def register_ship(parameters_dict: dict, session):
    new_ship = Ship(parameters["size"],
                    parameters_dict["color"],
                    parameters_dict["location"],
                    parameters_dict["gas"],
                    parameters_dict["crew"],
                    parameters_dict["crew-state"], 
                    parameters_dict["damage"] 
                    )
    
    # Save on database
    
    FileReader.save_file(session.cache["ship_data_path"], dict_to_csv(parameters_dict))

    return new_ship

ship = register_ship(parameters)
