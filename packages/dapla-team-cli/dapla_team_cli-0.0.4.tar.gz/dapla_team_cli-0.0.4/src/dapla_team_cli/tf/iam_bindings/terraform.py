"""Module that contains terraform related functions."""
import os
import re
from typing import Any
from typing import Dict
from typing import List

import tfvars
from rich.console import Console
from rich.style import Style

from dapla_team_cli.team import TeamInfo
from dapla_team_cli.tf.iam_bindings import IAMBindingConfig
from dapla_team_cli.tf.iam_bindings import jinja_env
from dapla_team_cli.tf.iam_bindings.buckets import (
    filter_buckets,  # TODO: Restructure this?
)


console = Console()

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def parse_team_info(team_repo_path: str) -> TeamInfo:
    """Retrieve team info and organization number from .tfvars file.

    Args:
        team_repo_path: The team repo path where the terraform.tfvars file is contained.

    Returns:
        The team info retrieved from file.
    """
    path_to_tfvars = team_repo_path + "/terraform.tfvars"
    tfv = tfvars.LoadSecrets(path_to_tfvars)

    with open(path_to_tfvars, encoding="UTF-8") as tf_vars_content:
        match = re.search(r"organizations\/(\w{12})\/roles", tf_vars_content.read())
        assert match is not None
        org_no = match.group(1)

    return TeamInfo(name=tfv["team_name"], org_no=org_no)


def write_tf_files(config: IAMBindingConfig, target_path: str) -> List[Any]:
    """Produce and write terraform files to `target_path`.

    Args:
        config: user supplied configuration
        target_path: The path to write files to

    Returns:
        a list of terraform files that was written
    """
    # Create terraform files - one file per auth group and environment
    tf_files = create_tf_files(config)
    target_tf_files = []

    # Write the files to the team's IaC repo
    for tf_file_name, content in tf_files.items():
        file_path = os.path.join(target_path, tf_file_name)
        with open(file_path, mode="w", encoding="utf-8") as tf_file:
            tf_file.write(content)
            target_tf_files.append(tf_file)

    return target_tf_files


def create_tf_files(config: IAMBindingConfig) -> Dict[str, str]:
    """Create Terraform files (iam-bindings) based on user-specified resource configuration.

    Args:
        config: IAMBindingConfig collected from user that specifies which resources to
            generate Terraform IAM bindings for

    Returns:
        An IAMBindingConfig (filename -> tf file content)

    """
    tf_files = {}
    template = jinja_env.get_template("iam-bindings-for-group-and-env.tf.jinja")
    team_name = config.team_name
    for env in config.environments:
        read_buckets = filter_buckets(config.buckets, "read", env, team_name)
        write_buckets = filter_buckets(config.buckets, "write", env, team_name)

        if any(li for li in [config.project_roles, read_buckets, write_buckets]):
            filename = f"iam-{config.auth_group.shortname}-{env}.tf"
            tf_files[filename] = template.render(
                env=env,
                auth_group=config.auth_group.name,
                auth_group_shortname=config.auth_group.shortname,
                project_roles=config.project_roles,
                read_buckets=read_buckets,
                org_no=config.org_no,
                write_buckets=write_buckets,
                expiry=config.expiry,
            )

    return tf_files
