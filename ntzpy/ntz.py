# add your code in this file
import os
from typing import Any, Dict, NamedTuple
from pathlib import Path

from ntzpy.database import DatabaseHandler


class ToDo(NamedTuple):
  todo: Dict[str, Any]
  error: int


class ToDoer:
  def __init__(self, db_path: Path) -> None:
    self.db_handler = DatabaseHandler(db_path)

# main function


def cli():
  pass


def get_args():
  return os.sys.argv
  
# run the main function
cli()
