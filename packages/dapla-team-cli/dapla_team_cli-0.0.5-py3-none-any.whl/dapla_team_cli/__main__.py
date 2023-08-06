"""Command-line interface.

CLI commands are generally structured according to this convention:
<root> <command-group> <command>

Example:
    Given the command ´dpteam tf iam-bindings´ then...
    ´dpteam´ is the root (CLI name)
    ´tf´ is the command group and
    ´iam-bindings´ is the actual command

Command groups must be mounted here to become available.

Each sub-command's modules should be grouped into a separate python package.
"""
from importlib.metadata import version
from typing import Optional

import typer

import dapla_team_cli.auth as auth
import dapla_team_cli.doctor as doctor
import dapla_team_cli.groups as groups
import dapla_team_cli.secrets as secrets
import dapla_team_cli.tf as tf


app = typer.Typer(no_args_is_help=True)


__version__ = version("dapla_team_cli")


def version_cb(value: bool) -> None:
    """Prints the current version of dapla-team-cli."""
    if value:
        print(f"dapla-team-cli {__version__}")
        raise typer.Exit()


@app.callback()
def dpteam(version: Optional[bool] = typer.Option(None, "--version", callback=version_cb, is_eager=True)) -> None:  # noqa: B008
    """Work seamlessly with Dapla teams from the command line.

    \b

    Use `dpteam <command> <subcommand> --help` for more information about a command.

    For an introduction to Dapla Team CLI, read the guide at https://statisticsnorway.github.io/dapla-team-cli/guide
    """
    pass


def main() -> None:
    """Main function of dpteam."""
    app()


app.add_typer(tf.app)
app.add_typer(groups.app)
app.add_typer(secrets.app)
app.add_typer(auth.app)

app.command()(doctor.doctor)

if __name__ == "__main__":
    main()
