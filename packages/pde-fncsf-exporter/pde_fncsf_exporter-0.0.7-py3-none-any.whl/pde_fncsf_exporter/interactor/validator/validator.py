#! /usr/bin/python3
#
# validator.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
The validator is a light (lighter than Great Expectations) mechanism to validate the dataframes
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import Any, Dict, Generator, Optional, Tuple

import pandas as pd

from pde_fncsf_exporter.errors import Errors
from pde_fncsf_exporter.logger import MixinLogable

#############################################################################
#                                 Classes                                   #
#############################################################################


class Validator(MixinLogable):
    """
    Holds suits of rules to validate the dataframes
    """

    _expectations_store = {}

    @classmethod
    def register(cls, *, name: str):
        """
        Decorator to register a validation function
        """

        def _(func):
            cls._expectations_store[name] = func
            return func

        return _

    def __init__(self, *expections: Tuple[str, Dict[str, Any]]):
        """
        Initialize the validator

        Args:
            expections (Iterable[Callable]): The rules to apply
        """

        super().__init__(logger_name="Validator")
        self._expectations = expections

    def __call__(self, df: pd.DataFrame) -> Generator[str, None, None]:
        """
        Validate the dataframe against the given rules

        Args:
            df (pd.DataFrame): The dataframe to validate
        """

        def _() -> Generator[str, None, None]:
            for rule_name, kwargs in self._expectations:

                # Fetch the rule from the store
                rule = self._expectations_store.get(rule_name, None)
                if not rule:
                    raise Errors.E030(rule_name=rule_name)  # type: ignore

                self.debug(f'Applying rule {rule.__name__}"')
                result = rule(df, **kwargs)
                if result is not None:
                    yield result

        return _()


def validate_csv(df: pd.DataFrame, validator: Validator) -> Optional[str]:
    """
    Check and validate the file located at path.

    Args:
        df (pd.DataFrame): The pandas dataframe
        validator (Validator): The validator to use
    """

    for error in validator(df):
        if error is not None:
            return error
