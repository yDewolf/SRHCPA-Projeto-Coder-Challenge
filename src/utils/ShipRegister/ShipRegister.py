# Ship registration utils
import utils.fileUtils.FileUtils as FileUtils
from utils.fileUtils.CsvUtils import dict_to_csv
from Ship import Ship

def register_ship(parameters_dict: dict, session):
    new_ship = Ship(parameters_dict["size"],
                    parameters_dict["color"],
                    parameters_dict["location"],
                    parameters_dict["gas"],
                    parameters_dict["crew"],
                    parameters_dict["crew-state"], 
                    parameters_dict["damage"] 
                    )
    
    # Save on database
    
    FileUtils.save_file(session.cache["ship_data_path"], "\n" + dict_to_csv(parameters_dict), overwrite=False)

    return new_ship
