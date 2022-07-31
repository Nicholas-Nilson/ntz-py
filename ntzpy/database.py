
"""Provides database functionality for NTZ"""

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from ntzpy import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS


# notes will be a list of dictionaries, each representing a to-do
class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:

    # DatabaseHandler will do the reading & writing, when it's initialized it just
    # needs to konw where this is all happening.
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
    # below to read & write to our JSON db.
    # read_todos opens the db and deserializes it (takes from JSON format
    # and turns it in to something we can natively use in Python).

    def read_todos(self) -> DBResponse:
        try:
            with self.db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError: # to catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError: # catch IO issues
            return DBResponse( [], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        """Takes a dictionary input to add to the database of to-dos"""
        try:
            with self.db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError: #catch IO issues
            return DBResponse(todo_list, DB_WRITE_ERROR)


# if the user does not specify a save location for the database, this will generate a default.
DEFAULT_DB_FILE_PATH = Path.home().joinpath("."+Path.home().stem + "_todo.json")


# generates the path to the database based on current app location & config file.
def get_database_path(config_file: Path) -> Path:
    """Returns the current path of the app's database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the database"""
    try:
        db_path.write_text("[]") #Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

