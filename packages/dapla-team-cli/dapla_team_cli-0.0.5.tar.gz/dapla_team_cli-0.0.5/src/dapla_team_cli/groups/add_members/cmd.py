"""Groups CLI command definition."""
import json
import sys
from typing import Any
from typing import List
from typing import Optional

import questionary as q
import requests
import typer
from rich.console import Console
from rich.style import Style

from dapla_team_cli import prompt_custom_style
from dapla_team_cli.auth.services.get_token import get_token
from dapla_team_cli.config import DAPLA_TEAM_API_BASE
from dapla_team_cli.groups.services.list_groups import deduce_team_info
from dapla_team_cli.tf.iam_bindings import MissingUserSuppliedInfoError
from dapla_team_cli.tf.iam_bindings.auth_groups import AuthGroupValidator
from dapla_team_cli.tf.iam_bindings.cmd import ask_for_iac_repo


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def add_members(
    team_name: Optional[str] = typer.Option(  # noqa: B008
        None,
        "--team-name",
        "-tn",
        help="Name of the auth group that the member(s) should be added to, such as 'demo-enhjoern-a-support'",
    ),
    group_name: Optional[str] = typer.Option(  # noqa: B008
        None, "--group-name", "-gn", help="Dapla team name, such as 'demo-enhjoern-a'"
    ),
) -> None:
    """Add new member(s) to the provided auth group."""
    print("What auth group would you like to add new members to?")

    if not team_name:
        team = deduce_team_info()
        team_name = team.name
        if not team_name:
            team_name = ask_for_iac_repo()
            team_name = team_name.rsplit("/", maxsplit=1)[-1]

    if not team_name:
        raise MissingUserSuppliedInfoError("Not an IaC repo and no team_name supplied, nothing to do...")

    if not group_name:
        group_name = _ask_for_auth_group(team_name)

    if not group_name:
        raise MissingUserSuppliedInfoError("No groups were provided, could not complete request...")

    print("Who would you like to add?")

    members = _ask_for_members()

    api_endpoint = DAPLA_TEAM_API_BASE + f"groups/{group_name}"
    auth_token = get_token()

    for member in members:
        payload = {"emailShort": f"{member}"}  # type: Any
        payload = json.dumps(payload)
        data = requests.patch(
            api_endpoint,
            payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"},
            timeout=10,
        )

        if data.status_code == 200:
            data = data.json()
        else:
            console.print(
                f"Error with status code: {data.status_code}. There was an error processing your request.",
                style=styles["warning"],
            )
            console.print(
                "Please ensure that you have a valid token by re-running 'dpteam auth login' with a fresh token.",
                style=styles["warning"],
            )
            sys.exit(1)


def _ask_for_members() -> List[str]:
    """Ask for which members to add to a group. Members consist of all SSB employees.

    Returns:
        Returns a set of members to add.
    """
    auth_token = get_token()

    api_endpoint = DAPLA_TEAM_API_BASE + "users"
    data = requests.get(api_endpoint, headers={"Authorization": f"Bearer {auth_token}"}, timeout=10)

    if data.status_code == 200:
        data = data.json()
    else:
        console.print(
            f"Error with status code: {data.status_code}. There was an error processing your request.",
            style=styles["warning"],
        )
        console.print(
            "Please ensure that you have a valid token by re-running 'dpteam auth login' with a fresh token.",
            style=styles["warning"],
        )
        sys.exit(1)

    data = data["_embedded"]["userList"]

    choices = [f'{item["name"]} - {item["emailShort"]}' for item in data]
    meta_information = {}

    for item in data:

        meta_information[f"{item}"] = f"{item['name']} - {item['email']}"

    q.print("(hit enter when done)")
    members_set = set()
    while True:
        member_short_email = q.autocomplete(
            message="Member name",
            choices=choices,
            meta_information=meta_information,
            style=prompt_custom_style,
        ).ask()
        if member_short_email:

            member_short_email = member_short_email.split("-")[1].strip()
            members_set.add(member_short_email)
        else:
            break

    return list(members_set)


def _ask_for_auth_group(team_name: str) -> str:
    """Ask user for the auth group that the new members should be added to.

    Args:
        team_name: The name of the dapla team.

    Returns:
        The auth group the members should be added to.
    """
    auth_group = q.select(
        message="Auth Group",
        instruction="(name of the Auth group the members should be added to)",
        qmark="👥",
        choices=[
            q.Choice(auth_group, value=auth_group)
            for auth_group in [
                f"{team_name}-support",
                f"{team_name}-developers",
                f"{team_name}-data-admins",
                f"{team_name}-managers",
                "Other...",
            ]
        ],
    ).ask()

    if auth_group == "Other...":
        auth_group = q.text(
            message="Custom Auth Group",
            validate=AuthGroupValidator,
        ).ask()

    return str(auth_group)
