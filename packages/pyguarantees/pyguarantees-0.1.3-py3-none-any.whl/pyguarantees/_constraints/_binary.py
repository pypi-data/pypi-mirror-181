from dataclasses import dataclass

from ._base import _TypeGuarantee
from pyguarantees._constraints._util.common_checks import \
    enforce_dynamic_checks, check_type, check_forbidden_values


@dataclass
class _IsBytes(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsBytes"
        self.guaranteed_type = bytes

    def enforce(self, arg) -> bytes:
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsByteArray(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsByteArray"
        self.guaranteed_type = bytearray

    def enforce(self, arg) -> bytearray:
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsMemoryView(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsMemoryView"
        self.guaranteed_type = memoryview

    def enforce(self, arg) -> memoryview:
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg

