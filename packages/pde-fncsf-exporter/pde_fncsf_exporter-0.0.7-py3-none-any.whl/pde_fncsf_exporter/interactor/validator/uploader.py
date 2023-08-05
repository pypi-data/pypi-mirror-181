#! /usr/bin/python3
#
# uploader.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Collections of functions to be binded to the CLI
"""

#############################################################################
#                                 Packages                                  #
#############################################################################


from pathlib import Path

import awswrangler as wr
import boto3
import pandas as pd
import csv

from pde_fncsf_exporter.api.credentials import get_credentials, Credentials
from pde_fncsf_exporter.errors import Errors
from pde_fncsf_exporter.interactor import validate_csv
from pde_fncsf_exporter.interactor.validator import parse_targets
from pde_fncsf_exporter.logger import get_module_logger

#############################################################################
#                                  Script                                   #
#############################################################################


_LOGGER = get_module_logger("uploader")
_BUCKET = "pde-integration/landing-zone"
_TARGETS = parse_targets()


_SCHEMA = {}
_SCHEMA["schools"] = {
    "school_id": pd.StringDtype(),
    "school_year": pd.Int64Dtype(),
    "school_name": pd.StringDtype(),
    "adress": pd.StringDtype(),
    "city": pd.StringDtype(),
    "postal_code": pd.StringDtype(),
}

_SCHEMA["students"] = {
    "school_id": pd.StringDtype(),
    "levels": pd.Int64Dtype(),
    "school_year": pd.Int64Dtype(),
    "number_of_students": pd.Int64Dtype(),
}

_SCHEMA["job_postings"] = {
    "title": pd.StringDtype(),
    "contract_type": pd.Int64Dtype(),
    "fte": pd.Float64Dtype(),
    "posting_start_date": pd.StringDtype(),
    "posting_end_date": pd.StringDtype(),
    "hired": pd.Int64Dtype(),
    "school_id": pd.StringDtype(),
}

_SCHEMA["teachers"] = {
    "teacher_id": pd.StringDtype(),
    "school_year": pd.Int64Dtype(),
    "fte": pd.Float64Dtype(),
    "qualifications": pd.Int64Dtype(),
    "speciality": pd.Int64Dtype(),
    "contract_type": pd.Int64Dtype(),
    "contract_start_date": pd.StringDtype(),
    "contract_end_date": pd.StringDtype(),
    "retirement": pd.Int64Dtype(),
    "school_id": pd.StringDtype(),
}


def _format_data(df: pd.DataFrame, key: str, credentials: Credentials) -> pd.DataFrame:
    """
    Set the appropriate data types.
    """

    df = df.copy()

    schema = _SCHEMA.get(key, None)
    if not schema:
        _LOGGER.info(f"\U0000270B Missing schema specification for artifact `{key}`.")
    else:
        try:
            df = df.astype(schema)
        except BaseException as error:
            raise Errors.E023(name=key) from error  # type: ignore

    # Prepare the dataframe by adding the required fields
    df["id_org"] = credentials.id_org
    df["inserted_date"] = pd.Timestamp.now()

    return df


def _upload_to_s3(df: pd.DataFrame, key: str, credentials: Credentials) -> None:
    """
    Upload the file to s3
    """

    # Storing data on Data Lake
    try:
        wr.s3.to_csv(
            df=df,
            boto3_session=boto3.Session(aws_access_key_id=credentials.access_key, aws_secret_access_key=credentials.secret_key),
            path=f"s3://{_BUCKET}/{credentials.username}/{key}",
            dataset=True,
            mode="overwrite",
            sanitize_columns=True,
            index=False,
            compression="gzip",
            # quoting=csv.QUOTE_NONNUMERIC,
            encoding="utf-8",
        )
    except BaseException as error:
        raise Errors.E040() from error  # type: ignore


def upload(path: Path) -> None:
    """
    Run the validations on the dataframes

    Args:
        path (Path): The base path to be used
    """

    credentials = get_credentials()
    if credentials is None:
        return

    for target in _TARGETS:

        target_path = path / target.path

        _LOGGER.info(f"\U00002699 Processing {target.name} ...")
        if not target_path.exists():
            raise Errors.E010(path=path)  # type: ignore

        try:
            df = pd.read_csv(target_path, encoding="utf-8")
        except BaseException as err:
            raise Errors.E022(path=target_path) from err  # type: ignore

        formatted = _format_data(df, target.name, credentials)
        out = validate_csv(formatted, target.validator)

        if out is not None:
            _LOGGER.error(f'\U0000274C Validation failed for "{target.name}" \U0000274C')
            _LOGGER.error(" - \t" + out)
            return
        _LOGGER.info(f"\U00002728 {target.name} has been validated.")

        _upload_to_s3(df, target.name, credentials)
        _LOGGER.info(f"\U0001F680 {target.name} has been synced with the platform.")


if __name__ == "__main__":
    upload(Path.cwd())
