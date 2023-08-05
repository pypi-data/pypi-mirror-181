#! /usr/bin/python3
#
# cli.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Centralize errors for the statisfactory package
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pathlib import Path

import click

# Project related packages
from pde_fncsf_exporter.api.credentials import store_credentials
from pde_fncsf_exporter.interactor.validator.uploader import upload

#############################################################################
#                                Constants                                  #
#############################################################################


@click.group()
def cli():
    """
    FNCSF PDE Data Exporter.

    The exporter contains two commands : 'configure' and 'export'.

    * Use 'configure' to configure the client for the first time. You will be asked the credentials provided by the FNCSF.

    * Use 'export' to sync your local datas to the platform. The exporter must have been configured before hand.
    """
    pass


@cli.command()
@click.option("--access_key", type=click.STRING, prompt="The ACCESS key")
@click.option("--secret_key", type=click.STRING, prompt="The SECRET key")
def configure(access_key: str, secret_key: str):
    """
    Configure the data exporter.
    If existing, the credentials will be overidded

    Args:
        access_key (str): The access key you have been provided with.
        secret_key (str): The secret key associated to your access key.
    """

    store_credentials(access_key=access_key, secret_key=secret_key)


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def export(path: Path):
    """
    Sync the datasets with the FNCSF's platform

    Args:
        path (Path): The path the .csvs are located. Use 'export .' to use the current folder.
    """

    path = Path(path)
    upload(path)
