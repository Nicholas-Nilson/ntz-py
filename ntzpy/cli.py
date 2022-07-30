from pathlib import Path
from typing import Optional, List
import typer

import ntzpy
import ntzpy.ntz
from ntzpy import __app_name__, __version__, ERRORS, config, database

app = typer.Typer()


# init is a typer command, using the app.command decorator.
@app.command()
def init(
        db_path: str = typer.Option(
            # prompt user with command for setting up database.
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="to-do database location?"
        ),
) -> None:
    """Initialize the to-do database"""
    app_init_error = config.init_app(db_path)
    # try calling the init file, if it doesn't work, throw the following errors based on given criteria
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"To ntz to-do database is {db_path}", fg=typer.colors.GREEN)


def get_todoer() -> ntzpy.ntz.ToDoer:
    # check for config file to ensure the db path is properly routed
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not fount. Please run "ntz init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    # likewise, if we have a config file, does it have a db_path? if so, let's send the
    # to do lists there, otherwise let's ask the user to run init.from
    # if both the config & db_path exist, we create an instance of our to do list maker
    if db_path.exists():
        return ntzpy.ntz.ToDoer(db_path)
    else:
        typer.secho(
            'Database not found. Please run "ntz init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)



def _version_callback(value):
    if value:
        typer.echo("-----------------------------ntzpy----------------------------")
        typer.echo(f"{__app_name__} v{__version__}\n")
        typer.echo("\nWhere notes are made and labs are completed")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

