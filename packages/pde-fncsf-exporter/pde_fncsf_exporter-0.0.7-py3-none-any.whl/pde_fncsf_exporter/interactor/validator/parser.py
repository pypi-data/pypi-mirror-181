#! /usr/bin/python3
#
# parser.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Parse the targets to be used for the dataframes validation.
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pathlib import Path
from pydantic.dataclasses import dataclass
from typing import Any, Dict, Any, List
import yaml
from pde_fncsf_exporter.interactor.validator.validator import Validator
from pde_fncsf_exporter.errors import Errors

#############################################################################
#                                  Script                                   #
#############################################################################


class _config:
    """
    Config for the Target dataclasses.
    """

    arbitrary_types_allowed = True


@dataclass(config=_config)
class Target:
    """
    Represent a target to be validated.
    """

    @dataclass
    class Expectations:
        """
        Holds the parameters of a an Expectation to be checked againsta a dataframe
        """

        name: str
        params: Dict[str, Any]

    name: str
    path: str
    expectations: List[Expectations]

    @property
    def validator(self) -> Validator:
        """
        Instanciate the Validator from the parsed expectations.
        """
        return Validator(*[(e.name, e.params) for e in self.expectations])


def parse_targets() -> List[Target]:
    """
    Parse the `targets.json` file and return the expectations to be used against the dataframe.

    Returns:
        Dict[str, Any]: The parsed Targets.
    """

    # Raw parse the file
    targets_path = Path(__file__).parent / "targets.yml"
    try:
        with open(targets_path) as f:
            targets = yaml.load(f, Loader=yaml.FullLoader)
    except BaseException as error:
        raise Errors.E013() from error  # type: ignore

    # Parse the targets
    return [Target(**target) for target in targets]
