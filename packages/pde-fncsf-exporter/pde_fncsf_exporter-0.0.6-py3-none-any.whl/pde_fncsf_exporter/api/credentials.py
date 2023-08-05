#! /usr/bin/python3
#
# configurator.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Writes and validate the AWS key configuration
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import Optional
import json
from dataclasses import dataclass
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from pde_fncsf_exporter.errors import Errors
from pde_fncsf_exporter.logger import get_module_logger

#############################################################################
#                                  Script                                   #
#############################################################################

CONFIG_FILE = Path.home() / ".pde-exporter" / "credentials.json"
_LOGGER = get_module_logger("configurator")


@dataclass
class Credentials:
    """
    Holds the AWS credentials
    """

    access_key: str
    secret_key: str
    username: str
    id_org: int
    email: str


def get_credentials() -> Optional[Credentials]:
    """
    Fetch the crendentials for the user
    """

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as file:
            credentials = json.load(file)
        return Credentials(**credentials)
    else:
        _LOGGER.error("\U000026A0 No credentials has been found. Please call the `pde_fncsf_exporter configure` command first. \U000026A0")
        return


def store_credentials(access_key: str, secret_key: str) -> None:
    """
    Store the AWS credentials

    Args:
        access_key (str): The access key to use to connect to AWS.
        secret_key (str): The secret key to use to connect to AWS.
    """

    # Fetch the username to be stored alongside the Creds
    _LOGGER.debug("Checking credentials.")
    try:
        user = boto3.client("iam", aws_access_key_id=access_key, aws_secret_access_key=secret_key).get_user()["User"]
        tags = {item["Key"]: item["Value"] for item in user["Tags"]}
        tags["username"] = user["UserName"]
    except ClientError:
        _LOGGER.error("Invalid credentials")
        return
    _LOGGER.debug(f"Extracted tags : {tags}")

    credentials = Credentials(access_key=access_key, secret_key=secret_key, **tags)
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as file:
            json.dump(credentials.__dict__, file)
    except BaseException as error:
        raise Errors.E011(path=str(CONFIG_FILE)) from error  # type: ignore

    _LOGGER.info("\U0001F44D Credentials has been successfully stored.")
