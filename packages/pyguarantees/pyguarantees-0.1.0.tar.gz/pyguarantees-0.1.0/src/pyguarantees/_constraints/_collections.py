from dataclasses import dataclass
from typing import Any, List

from ._base import _TypeGuarantee
from pyguarantees._constraints._util.common_checks import \
    enforce_dynamic_checks, check_type, check_forbidden_values
from pyguarantees._constraints._util.collections_checks import \
    check_minmax_len, check_contains, check_has_keys_values


@dataclass
class _CollectionType(_TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None


@dataclass
class _IsList(_CollectionType):
    contains: List[Any] = None

    def __post_init__(self):
        self.guarantee_name = "IsList"
        self.guaranteed_type = list

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        check_minmax_len(arg, self)
        check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsTuple(_CollectionType):
    contains: List[Any] = None

    def __post_init__(self):
        self.guarantee_name = "IsTuple"
        self.guaranteed_type = tuple

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        check_minmax_len(arg, self)
        check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsDict(_CollectionType):
    has_keys: List[Any] = None
    has_values: List[Any] = None

    def __post_init__(self):
        self.guarantee_name = "IsDict"
        self.guaranteed_type = dict

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        check_minmax_len(arg, self)
        check_has_keys_values(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsSet(_CollectionType):
    contains: Any = None

    def __post_init__(self):
        self.guarantee_name = "IsSet"
        self.guaranteed_type = set

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        check_minmax_len(arg, self)
        check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsFrozenSet(_CollectionType):
    contains: Any = None

    def __post_init__(self):
        self.guarantee_name = "IsFrozenSet"
        self.guaranteed_type = frozenset

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        check_minmax_len(arg, self)
        check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsRange(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsRange"
        self.guaranteed_type = range

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg
