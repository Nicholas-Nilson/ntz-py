
"""Provides database functionality for NTZ"""

import configparser
from pathlib import Path

from ntzpy import DB_WRITE_ERROR, SUCCESS


# if the user does not specify a save location for the database, this will generate a default.
DEFAULT_DB_FILE_PATH = Path.home().joinpath("."+Path.home().stem + "_todo.json")


# generates the path to the database based on current app location & config file.
def get_database_path(config_file: Path) -> Path:
    """Returns the current path of the app's database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["general"]["database"])


def init_database(db_path: Path) -> int:
    """Create the database"""
    try:
        db_path.write_text("[]") #Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

