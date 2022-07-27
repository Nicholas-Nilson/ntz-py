from typing import Optional
import typer

from ntzpy import __app_name__, __version__

app = typer.Typer()


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

