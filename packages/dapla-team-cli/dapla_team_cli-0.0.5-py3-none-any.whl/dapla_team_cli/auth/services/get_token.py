"""Get token helper function. Retrieve the Keycloak token on local machine."""
import json
import os
import sys
from typing import Union

import requests
from jupyterhub.services.auth import HubAuth
from rich.console import Console
from rich.style import Style

from dapla_team_cli.config import get_config_folder_path


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def get_token() -> Union[str, None]:
    """Retrieves token if it exists or returns None if no token exists.

    Returns:
        Either the Keycloak token, if it exists, or None if it does not exist.
    """
    # Taken from dapla-toolbelt
    if os.getenv("NB_USER") == "jovyan":
        hub = HubAuth()
        response = requests.get(
            os.environ["LOCAL_USER_PATH"],
            headers={"Authorization": "token %s" % hub.api_token},
            cert=(str(hub.certfile), str(hub.keyfile)),
            verify=str(hub.client_ca),
            allow_redirects=False,
        )
        if response.status_code == 200:
            token = str(response.json()["access_token"])
            if token:
                return token

    config_folder_path = get_config_folder_path()
    config_file_path = config_folder_path + "/dapla-cli-keycloak-token.json"

    if os.path.isfile(config_file_path):
        with open(config_file_path, encoding="UTF-8") as f:
            data = json.loads(f.read())
            keycloak_token = data["keycloak_token"]
    else:
        console.print("No valid access token found. Please run 'dpteam auth login' first.", style=styles["warning"])
        sys.exit(1)

    return str(keycloak_token)
