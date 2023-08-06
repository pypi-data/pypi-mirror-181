"""Terraform related commands.

Commands invoked by dpteam tf <some-command> are defined here.
"""
import typer

import dapla_team_cli.tf.iam_bindings.cmd as iam_bindings


app = typer.Typer(no_args_is_help=True)


@app.callback()
def tf() -> None:
    """Inspect and modify a team's Terraform code."""
    pass


app.command()(iam_bindings.iam_bindings)
