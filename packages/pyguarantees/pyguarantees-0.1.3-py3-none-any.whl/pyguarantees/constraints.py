from dataclasses import dataclass

from pyguarantees._constraints._base import (
    _Guarantee,
    _TypeGuarantee
)
from pyguarantees._constraints._binary import (
    _IsBytes,
    _IsMemoryView,
    _IsByteArray
)
from pyguarantees._constraints._boolean import _IsBool
from pyguarantees._constraints._collections import (
    _IsList,
    _IsTuple,
    _IsDict,
    _IsSet,
    _IsFrozenSet,
    _IsRange
)
from pyguarantees._constraints._dynamic_check import _DynamicCheck
from pyguarantees._constraints._numeric import (
    _IsInt,
    _IsFloat,
    _IsComplex
)
from pyguarantees._constraints._other import (
    _NoOp,
    _Cls,
    _Self,
    _IsNone,
    _IsUnion,
    _IsClass
)
from pyguarantees._constraints._string import _IsStr


@dataclass
class Guarantee(_Guarantee):
    pass


@dataclass
class TypeGuarantee(_TypeGuarantee, Guarantee):
    pass


@dataclass
class GuaranteeInternal(TypeGuarantee):
    def __post_init__(self):
        self.guaranteed_type = None
        self.guarantee_name = "GuaranteeInternal"


@dataclass
class DynamicCheck(_DynamicCheck):
    pass


@dataclass
class IsBytes(_IsBytes, TypeGuarantee):
    pass


@dataclass
class IsByteArray(_IsByteArray, TypeGuarantee):
    pass


@dataclass
class IsMemoryView(_IsMemoryView, TypeGuarantee):
    pass


@dataclass
class IsBool(_IsBool, TypeGuarantee):
    pass


@dataclass
class IsList(_IsList, TypeGuarantee):
    pass


@dataclass
class IsTuple(_IsTuple, TypeGuarantee):
    pass


@dataclass
class IsDict(_IsDict, TypeGuarantee):
    pass


@dataclass
class IsSet(_IsSet, TypeGuarantee):
    pass


@dataclass
class IsFrozenSet(_IsFrozenSet, TypeGuarantee):
    pass


@dataclass
class IsRange(_IsRange, TypeGuarantee):
    pass


@dataclass
class IsInt(_IsInt, TypeGuarantee):
    pass


@dataclass
class IsFloat(_IsFloat, TypeGuarantee):
    pass


@dataclass
class IsComplex(_IsComplex, TypeGuarantee):
    pass

@dataclass
class IsClass(_IsClass, TypeGuarantee):
    pass


@dataclass
class NoOp(_NoOp, Guarantee):
    pass


@dataclass
class Self(_Self, NoOp):   # so that it's ignored
    pass


@dataclass
class Cls(_Cls, NoOp):   # so that it's ignored
    pass


@dataclass
class IsNone(_IsNone, TypeGuarantee):
    pass


@dataclass
class IsUnion(_IsUnion, TypeGuarantee):
    pass


@dataclass
class IsStr(_IsStr, TypeGuarantee):
    pass
