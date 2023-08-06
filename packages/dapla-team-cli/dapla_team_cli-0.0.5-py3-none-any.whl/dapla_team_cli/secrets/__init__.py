"""GCP Secrets related commands.

Commands invoked by ´dpteam secrets <some-command>´ are defined here.
"""
import subprocess
from typing import Optional

import questionary as q
import typer

from dapla_team_cli.secrets.services import add_secret_version
from dapla_team_cli.secrets.services import request_secret_creation


app = typer.Typer(no_args_is_help=True)


@app.callback()
def secrets() -> None:
    """Manage a team's GCP secrets."""
    pass


@app.command()
def create(
    project_id: Optional[str] = typer.Option(None, "--payload", "-p", help="The secret data/payload"),  # noqa: B008
    secret_id: Optional[str] = typer.Option(None, "--secret-id", "-sid", help="ID of the secret, e.g. 'my-secret'"),  # noqa: B008
    payload: Optional[str] = typer.Option(  # noqa: B008
        None, "--project-id", "-pid", help="GCP project ID, e.g. 'dev-demo-example-1234'"
    ),
) -> None:
    """Create a new Secret Manager secret."""
    actual_pid: str = (
        q.text("What is the ID of the GCP project the secret should reside in?").ask() if project_id is None else project_id
    )
    actual_sid: str = q.text("Secret ID?").ask() if secret_id is None else secret_id
    actual_payload: str = q.text("Secret Payload?").ask() if payload is None else payload

    subprocess.run(["gcloud", "auth", "application-default", "login"], check=True)

    request_secret_creation(actual_pid, actual_sid)

    add_secret_version(actual_pid, actual_sid, actual_payload)

    print("The secret was successfully created")
