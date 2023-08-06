"""Terraform related commands.

Commands invoked by dpteam tf <some-command> are defined here.
"""
import click

from dapla_team_cli.tf.iam_bindings.cmd import iam_bindings


@click.group()
def tf() -> None:
    """Inspect and modify a team's Terraform code."""
    pass


tf.add_command(iam_bindings)
