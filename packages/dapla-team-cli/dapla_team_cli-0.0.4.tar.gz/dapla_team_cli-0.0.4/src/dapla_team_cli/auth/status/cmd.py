"""Authentication status command."""
from datetime import datetime
from datetime import timezone

import click
import jwt
from rich.console import Console
from rich.style import Style

from dapla_team_cli.auth.services.get_token import get_token


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


@click.command()
def status() -> None:
    """Show information about the current authentication status."""
    keycloak_token = get_token()

    if keycloak_token:
        dec_token = jwt.decode(keycloak_token, options={"verify_signature": False})
        expiry_date = datetime.fromtimestamp(dec_token["exp"], tz=timezone.utc)
        console.print(f"Identity: {dec_token['name']} <{dec_token['email']}>", style=styles["normal"])
        console.print(f"Expiry date: {expiry_date.astimezone().strftime('%Y/%m/%d %H:%M:%S')}", style=styles["normal"])
        if expiry_date < datetime.now(tz=timezone.utc):
            console.print("Your token has expired. Please run dpteam auth login to fetch a new one.", style=styles["warning"])
        console.print(f"Raw token: {keycloak_token}", no_wrap=True, style=styles["normal"])
    else:
        console.print(
            "You do not have a keycloak token set. Please run dpteam auth login --with-token <your_token> in order to add it.",
            style=styles["normal"],
        )
