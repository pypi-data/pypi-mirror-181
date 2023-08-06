"""Groups related commands.

Commands invoked by dpteam groups <some-command> are defined here.
"""

import typer

from dapla_team_cli.groups.add_members.cmd import add_members
from dapla_team_cli.groups.list_members.cmd import list_members


app = typer.Typer(no_args_is_help=True)


@app.callback()
def groups() -> None:
    """Interact with a team's auth group memberships."""
    pass


app.command()(add_members)
app.command()(list_members)
