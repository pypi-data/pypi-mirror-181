"""Login CLI command definition. Sets credentials on local machine for CLI user."""
import click

from dapla_team_cli.auth.services.set_token import set_token


@click.command()
@click.option(
    "keycloak_token",
    "--with-token",
    "-wt",
    help="Keycloak access token",
)
def login(keycloak_token: str) -> None:
    """Authenticate with Keycloak.

    The default authentication mode is a web-based browser flow. After
    completion, an access token will be stored internally.

    Alternatively, use `--with-token` to pass in a token on standard input.

    You need to be logged in to communicate with backend APIs
    such as the dapla-team-api.
    """
    set_token(keycloak_token)
