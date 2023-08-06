"""GCP Secrets related commands.

Commands invoked by ´dpteam secrets <some-command>´ are defined here.
"""
import click

from dapla_team_cli.secrets.create.cmd import create


@click.group()
def secrets() -> None:
    """Manage a team's GCP secrets."""
    pass


secrets.add_command(create)
