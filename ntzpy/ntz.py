# add your code in this file
import os
from typing import Any, Dict, NamedTuple, List
from pathlib import Path

from ntzpy import DB_READ_ERROR
from ntzpy.database import DatabaseHandler


class ToDo(NamedTuple):
  todo: Dict[str, Any]
  error: int


class ToDoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    # takes a description and priority. "Done" will be False by default.
    def add(self, description: List[str], priority: int = 2) -> ToDo:
        """Adds a new item to the database"""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        # if an error occurred, return the ToDo and the error
        if read.error == DB_READ_ERROR:
            return ToDo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        # if it all works out, return the ToDo and SUCCESS
        return ToDo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list

# main function


def cli():
  pass


def get_args():
  return os.sys.argv
  
# run the main function
cli()
