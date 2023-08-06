from dataclasses import dataclass

from ._base import _TypeGuarantee
from pyguarantees._constraints._util.common_checks import \
    enforce_dynamic_checks, check_type, check_forbidden_values


@dataclass
class _IsBool(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsBool"
        self.guaranteed_type = bool

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg
