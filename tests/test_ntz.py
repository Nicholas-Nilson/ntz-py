from typer.testing import CliRunner
import json
import pytest
from ntzpy import __app_name__, __version__, cli, DB_READ_ERROR, SUCCESS, ntz

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0  # ensures the application ran successfully
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
# tmp_path is a pathlib.Path object pytest uses for temporary purposes.
def mock_json_file(tmp_path):
    todo = [{"Description": "Get some milk.", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file


test_data1 = {
    "description": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}


@pytest.mark.parametrize(
    "description, priority, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    notez = ntz.ToDoer(mock_json_file)
    assert notez.add(description, priority) == expected
    read = notez._db_handler.read_todos()
    assert len(read.todo_list) == 2