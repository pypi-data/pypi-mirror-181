#! /usr/bin/python3
#
# errors.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Centralize errors for the statisfactory package
"""
# pylint: disable-all ## The code is too weird ;(
#############################################################################
#                                 Packages                                  #
#############################################################################

# System packages
import sys
import warnings

# Project related packages
from .logger import get_module_logger

#############################################################################
#                                Constants                                  #
#############################################################################

DEFAULT_LOGGER = get_module_logger(__name__)
PROJECT_NAME = "DataExporter"

#############################################################################
#                                 Classes                                   #
#############################################################################


class ExceptionFactory(type):
    """
    Implements a metaclass building errors from instances attributes. Errors are singleton and can be raised and catched.

    >>raise Errors.E010
    >>raise Errors.E010()
    """

    def __init__(cls, name, bases, attrs, *args, **kwargs):
        super().__init__(name, bases, attrs)
        super().__setattr__("_instance", None)
        super().__setattr__("_CACHED_ATTRIBUTES", dict())

    def __call__(cls, *args, **kwargs):
        if super().__getattribute__("_instance") is None:
            super().__setattr__("_instance", super().__call__(*args, **kwargs))
        return super().__getattribute__("_instance")

    def __getattribute__(cls, code):
        """
        Intercept the attribute getter to wrap the Error code in a metaclass. By doing so, the error code became
        a proper class for which the name is the error code
        """

        try:
            meta = super().__getattribute__("_CACHED_ATTRIBUTES")[code]
        except KeyError:

            # Retrieve the error message maching the code and preformat it
            msg = super().__getattribute__(code)
            msg = f"{PROJECT_NAME} : {code} - {msg}"

            proto = super().__getattribute__("_PROTOTYPE")
            meta = type(code, (proto,), {"msg": msg})
            super().__getattribute__("_CACHED_ATTRIBUTES")[code] = meta

        return meta


class ErrorPrototype(Exception):
    """
    Base parent for all custom errors raised by the program.
    The class performs base operation making the error message displaybale
    """

    msg: str = ""

    def __init__(self, **kwargs):

        super().__init__(self.msg.format(**kwargs))


class WarningPrototype(UserWarning):
    """
    Base parent for all custom warnings raised by the program.
    The class performs base operation making the warning displayba;e
    """

    msg: str = ""

    def __init__(self, **kwargs):

        super().__init__(self.msg.format(**kwargs))


class Errors(metaclass=ExceptionFactory):

    _PROTOTYPE = ErrorPrototype

    # Init errors
    E010 = "The artifact located at '{path}' does not exist."
    E011 = "Failed to store the credentails at '{path}'. Make sure you have the rights to write files at this location."
    E012 = "Failed to fetch the artifact. Please, call the configure command first."
    E013 = "Failed to load the target files."

    # Data related errors
    E022 = "Failed to open the artifact located at '{path}'. Make sure the file is a valid utf-8 encoded csv."
    E023 = "Failed to set the appropiate type for the dataframe '{name}'. Please make sure the data you have entered match their specifications."

    # Validator related errors
    E030 = "validator : the rule '{rule_name}' is not registered."
    E031 = "Validation Error : {msg}."

    # Export related errors
    E040 = "Failed to export the data to the plateform. Please, check the stacktrace for more information."


class Warnings(UserWarning):

    _PROTOTYPE = WarningPrototype

    # Instanciation
    W010 = "start-up : PYTHONPATH is already set and won't be overwritted by Statisfactoy : the sources from 'Lib' MIGHT not be reachable"


def _custom_formatwarning(msg, *args, **kwargs) -> str:
    """
    Monkey patch the warning displayor to avoid printing the code longside the Warnings.
    Monkeypatching the formatter is acutalyy the way to do it as recommanded by Python's documention.
    """
    return f"Warning : {str(msg)} \n"


warnings.formatwarning = _custom_formatwarning


if __name__ == "__main__":
    sys.exit()
