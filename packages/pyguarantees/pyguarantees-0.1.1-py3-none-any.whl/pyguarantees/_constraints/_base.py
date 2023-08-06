"""The base of the classes."""


import logging
from dataclasses import dataclass, field
from typing import Callable, Type, List
from pyguarantees import severity

from ._dynamic_check import _DynamicCheck


@dataclass
class _Guarantee:
    parameter_name: str = field(init=False)
    where: str = field(init=False)
    guarantee_name: str = field(init=False)
    guaranteed_type: Type = field(init=False)
    qualname: str = field(init=False)
    module: str = field(init=False)

    def enforce(self, arg):
        pass


@dataclass
class _TypeGuarantee(_Guarantee):
    force_conversion: bool = False
    logger: logging.Logger = None
    logger_only: bool = False
    error_severity: int = severity.ERROR
    error_callback: Callable = None
    dynamic_checks: List[_DynamicCheck] = None
    forbidden_values: list = None
