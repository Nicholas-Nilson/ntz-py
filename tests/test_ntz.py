from typer.testing import CliRunner
from ntzpy import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0  # ensures the application ran successfully
    assert f"{__app_name__} v{__version__}\n" in result.stdout
