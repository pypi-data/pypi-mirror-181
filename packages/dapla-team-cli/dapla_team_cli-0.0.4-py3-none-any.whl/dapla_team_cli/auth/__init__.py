"""Auth related commands.

Commands invoked by dpteam auth <some-command> are defined here.
"""

import click

from dapla_team_cli.auth.login.cmd import login
from dapla_team_cli.auth.status.cmd import status


@click.group()
def auth() -> None:
    """Authenticate dpteam with Keycloak."""
    pass


auth.add_command(login)
auth.add_command(status)
