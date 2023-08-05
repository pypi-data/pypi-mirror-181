from dataclasses import dataclass

from ._base import TypeGuarantee
from pyguarantees.functional_guarantees.classes.util.common_checks import \
    enforce_dynamic_checks, check_type


@dataclass
class IsBytes(TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsBytes"
        self.guaranteed_type = bytes

    def enforce(self, arg) -> bytes:
        arg = check_type(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsByteArray(TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsByteArray"
        self.guaranteed_type = bytearray

    def enforce(self, arg) -> bytearray:
        arg = check_type(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsMemoryView(TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsMemoryView"
        self.guaranteed_type = memoryview

    def enforce(self, arg) -> memoryview:
        arg = check_type(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg

