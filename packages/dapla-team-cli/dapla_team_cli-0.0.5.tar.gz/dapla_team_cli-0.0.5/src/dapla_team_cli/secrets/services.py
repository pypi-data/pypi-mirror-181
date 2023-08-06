"""Provides functions used to manage secrets."""

from typing import Any

from google.cloud import secretmanager


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
