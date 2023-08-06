"""Doctor related commands.

Commands invoked by dpteam doctor <some-command> are defined here.
"""

import subprocess
import sys
from sys import platform

import questionary as q
from rich.console import Console
from rich.style import Style

from dapla_team_cli.auth.services.get_token import get_token
from dapla_team_cli.auth.services.set_token import set_token


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "error": Style(color="red", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def doctor() -> None:
    """Check your system for potential problems.

    This could be e.g. if some required tooling is missing.
    The command provides advice and pointers to how to fix issues.
    Will exit with a non-zero status if any potential problems are found.
    """
    skipped_dependencies = False

    console.print("Checking for uninstalled dependencies...", style=styles["normal"])

    if platform == "darwin":

        brew_installation = subprocess.run(["brew", "--help"], capture_output=True, text=True, shell=False, check=True)

        if brew_installation.stderr:
            console.print("You are using MacOS, but you seem to be missing Homebrew...🍺", style=styles["normal"])
            console.print(
                "Please install Homebrew (https://brew.sh/) and verify your installation by "
                "running 'brew doctor'. Then rerun this command.",
                style=styles["normal"],
            )

            sys.exit(1)

        else:
            gcloud_installation = subprocess.run(["gcloud", "--help"], capture_output=True, text=True, shell=False, check=True)

            if gcloud_installation.stderr:
                console.print("The 'gcloud' CLI tool is required, but it seems to be missing.", style=styles["normal"])
                gcloud_permission = q.confirm("Do you want to install it?").ask()

                if gcloud_permission:

                    console.print("Installing Google Cloud CLI...", style=styles["normal"])

                    gcloud_installer = subprocess.run(
                        ["brew", "install", "--cask", "google-cloud-sdk"],
                        capture_output=False,
                        text=True,
                        shell=False,
                        check=True,
                    )

                    if gcloud_installer.stderr:
                        console.print("Something went wrong when trying to install gcloud with Homebrew...", style=styles["error"])

                        sys.exit(1)

                else:
                    skipped_dependencies = True

    keycloak_token_exists = get_token()

    if not keycloak_token_exists:
        permission_to_add_token = q.confirm("You do not have a valid Keycloak token. Do you wish to add it now?").ask()

        if permission_to_add_token:
            set_token(None)
        else:
            skipped_dependencies = True

    if skipped_dependencies:
        console.print(
            "You skipped some steps. Please re-run this command or add required dependencies manually.",
            style=styles["warning"],
        )

    else:
        console.print("Everything seems to be OK ✅", style=styles["success"])
