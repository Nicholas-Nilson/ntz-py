# add your code in this file
import os
from typing import Any, Dict, NamedTuple, List
from pathlib import Path

from ntzpy import DB_READ_ERROR, ID_ERROR
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

    def set_done(self, todo_id: int) -> ToDo:
        """Set a task to done"""
        read = self._db_handler.read_todos()
        if read.error:
            return ToDo({}, read.error)
        try:
            todo = read.todo_list[todo_id -1]
        except IndexError:
            return ToDo({}, ID_ERROR)
        # adding categories will require another argument todo["category"]["Done"]
        # can maybe add a letter prefix to IDs when created to just pass one.. A1 A2, B3...
        # etc. and just parse from there. thought
        # that would likely limit the categories to 26 unless we added logic to add another char to the prefix?
        todo["Done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return ToDo(todo, write.error)

    def remove(self, todo_id: int) -> ToDo:
        """Remove a to-do from the database using its id or index"""
        # read takes in the database
        read = self._db_handler.read_todos()
        if read.error:
            return ToDo({}, read.error)
        try:
            # with the passed in index we pop the specified ID
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return ToDo({}, ID_ERROR)
        # then write the updated list back to the database
        write = self._db_handler.write_todos(read.todo_list)
        return ToDo(todo, write.error)

    def remove_all(self) -> ToDo:
        """Clears database of all ToDos"""
        # uses db_handler to overwrite current database with an empty list
        write = self._db_handler.write_todos([])
        return ToDo({}, write.error)

# main function


def cli():
  pass


def get_args():
  return os.sys.argv
  
# run the main function
cli()
