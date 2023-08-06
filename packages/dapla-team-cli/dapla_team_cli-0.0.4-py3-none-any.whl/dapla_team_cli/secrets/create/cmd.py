"""Command for creating secrets in GCP Secret Manager."""
import subprocess
from typing import Any

import click
import questionary as q
from google.cloud import secretmanager


@click.command()
@click.option(
    "project_id",
    "--project_id",
    "-pid",
    help="GCP project ID, e.g. 'dev-demo-example-1234'",
)
@click.option(
    "secret_id",
    "--secret_id",
    "-sid",
    help="ID of the secret, e.g. 'my-secret'",
)
@click.option(
    "payload",
    "--playload",
    "-p",
    help="The secret data/payload",
)
def create(project_id: str, secret_id: str, payload: str) -> None:
    """Create a new Secret Manager secret."""
    if not project_id:
        project_id = q.text("What is the ID of the GCP project the secret should reside in?").ask()
    if not secret_id:
        secret_id = q.text("Secret ID?").ask()
    if not payload:
        payload = q.text("Secret Payload?").ask()

    subprocess.run(["gcloud", "auth", "application-default", "login"], check=True)

    request_secret_creation(project_id, secret_id)

    add_secret_version(project_id, secret_id, payload)

    print("The secret was successfully created")


def add_secret_version(project_id: str, secret_id: str, payload: Any) -> None:
    """Requests google cloud storage client to create a secret.

    Args:
        project_id: The ID of the project that the secret should be created in.
        secret_id: The ID of the secret to be created.
        payload: The payload of the secret to be created.
    """
    client = secretmanager.SecretManagerServiceClient()

    parent = client.secret_path(project_id, secret_id)

    payload = payload.encode("UTF-8")

    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": payload},
        }
    )

    print(f"Added secret version: {response.name}")


def request_secret_creation(project_id: str, secret_id: str) -> None:
    """Requests google cloud storage client to create a secret.

    Args:
        project_id: The ID of the project that the secret should be created in.
        secret_id: The ID of the secret to be created.
    """
    client = secretmanager.SecretManagerServiceClient()

    parent = f"projects/{project_id}"

    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    print(f"Created secret: {response.name}")
