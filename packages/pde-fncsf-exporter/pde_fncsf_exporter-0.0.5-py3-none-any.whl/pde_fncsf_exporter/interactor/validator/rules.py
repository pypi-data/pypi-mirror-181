#! /usr/bin/python3
#
# rules.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
A list of rules to be applied to the dataframes
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import List, Optional, Dict

import pandas as pd

from pde_fncsf_exporter.interactor.validator.validator import Validator
from pde_fncsf_exporter.logger import get_module_logger

#############################################################################
#                                 Script                                    #
#############################################################################

_LOGGER = get_module_logger("uploader")


@Validator.register(name="has_columns")
def _expectations_has_columns(df: pd.DataFrame, columns: List[str]) -> Optional[str]:
    """
    Check that the dataframes has the provided columns

    Args:
        df (pd.DataFrame): The dataframe to check
        columns (list[str]): A list of columns to check agains the dataframe.

    Returns:
        str: The list of missing columns, if any
    """

    missing_columns = set(columns) - set(df.columns)
    if missing_columns:
        return f"The dataset is missing the following columns: {', '.join(missing_columns)}"

    surnumerary_colunmns = set(df.columns) - set(columns)
    if surnumerary_colunmns:
        return f"The dataset has the following surnumerary columns: {', '.join(surnumerary_colunmns)}"

    return None


@Validator.register(name="has_types")
def _expectations_has_types(df: pd.DataFrame, want: Dict[str, str]) -> Optional[str]:
    """
    Check that the columns types are properly set.

    TODO : ignore empty columns
    Args:
        df (pd.DataFrame): The dataframe to check
        want (Dict[str, str]): A mapping of columns to their types.

    Returns:
        Optional[str]: A column not matching the type
    """

    got = df.dtypes
    got = {k: str(v) for k, v in got.items()}

    for column, want_type in want.items():
        got_type = got.get(column, None)
        if got_type is None:
            _LOGGER.warning(f"Column {column} is not present in the dataframe")
            continue

        if got_type != want_type:
            return f"Column {column} has type {got_type} but should be {want_type}"


@Validator.register(name="is_unique")
def _expectations_is_unique(df: pd.DataFrame, columns: List[str]) -> Optional[str]:
    """
    Check that the columns contains unique vlaues

    Args:
        df (pd.DataFrame): The dataframe to check
        column (str): The column to check

    Returns:
        Optional[str]: A column not matching the type
    """

    for col in columns:
        if not df[col].is_unique:
            return f"Column '{col}' contains duplicated values"
