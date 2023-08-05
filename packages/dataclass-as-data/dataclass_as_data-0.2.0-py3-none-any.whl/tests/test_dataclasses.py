from __future__ import annotations

from unittest.mock import Mock

from dataclasses import dataclass, field
from typing import Optional, Union
from enum import Enum, auto, IntEnum

from dataclass_as_data import DataAsTuple

__all__ = (
    'converter',

    # Basic testing
    'TestDataclassSimple',
    'TestDataclass',
    'TestDataclassTuple',

    'RecursiveTestDataclass',
    'RecursiveTestDataclassTuple',
    'RecursiveTestDataClassWithContainers',

    'TestDataclassWithStrictTuple',
    'TestDataclassWithOptionalParameters',
    'TestDataclassWithUnionParameter',
    'TestDataclassWithCustomConverter',
    'TestDataclassWithDataclassList',
    'TestDataclassWithUnionStartingWithStr',

    'LowerStr',

    'TestDataclassWithCustomClass',

    # Dataclasses for class polymorphism testing
    'ContainerDataclass',
    'BaseDataclass',
    'SubDataclassA',
    'SubDataclassB',
    'SubDataclassAsTuple',

    'BaseDataclassWithDefault',
    'SubDataclassAWithDefault',
    'SubDataclassBWithDefault',
    'SubDataclassWithDefaultAsTuple',

    'ContainerClassWithDefault',
    'ContainerClassWithUnionWithBaseClass',

    # Non-dataclass tests
    'NonDataclass',
    'DataclassWithNonDataclass',
    'DataclassWithByteArray',

    'HashableClass',
    'DataclassWithSetsOfDataclasses',

    'NonHashableClass',
    'DataclassWithListsOfNonDataclasses',

    'DataclassWithDictsOfNonDataclasses',

    'SubClassOfNonHashableClass',
    'DataclassWithSubClassOfNonDataclass',

    'DataclassOfPrimitives',

    'DataclassConverterTestAsTuple',

    # Dictionary key conversion tests
    'FrozenDataclass',
    'DataclassWithDataclassAsDictKeys',

    'FrozenDataclassWithFrozenDataclass',
    'DataclassWithRecursiveDataclassAsDictKeys',

    'DataclassWithClassAsDictKeys',

    'SubclassOfHashableClass',
    'DataclassWithSubclassAsDictKeys',

    # Misc
    'DataclassWithSets',

    'TestEnum',
    'DataclassWithEnum',

    'TestIntEnum',
    'DataclassWithIntEnum',

    'DataclassWithComplexTypesAsDictKeys',
)


converter = Mock()


## Dataclasses for basic testing
@dataclass
class TestDataclassSimple:
    number: int


@dataclass
class TestDataclass:
    number: int
    string: str = "ponies!"
    decimal: float = field(default=6.0, repr=False)

    _private: str = field(default="Shhh", repr=False, init=False)

    CONSTANT = "PONY"


@dataclass
class TestDataclassTuple(TestDataclass, DataAsTuple):
    pass


@dataclass
class RecursiveTestDataclass:
    number: int
    string: str = "ponies!"
    decimal: float = field(default=6.0, repr=False)

    test_dataclass: TestDataclass = TestDataclass(0)
    test_dataclass_tuple: TestDataclassTuple = TestDataclassTuple(1)

    _private: str = field(default="Shhh", repr=False, init=False)

    CONSTANT = "PONY"


@dataclass
class RecursiveTestDataclassTuple(RecursiveTestDataclass, DataAsTuple):
    pass


@dataclass
class RecursiveTestDataClassWithContainers:
    numbers: list[int]
    objects: dict[str, TestDataclass]
    extra_objects: list[TestDataclassTuple] = field(default_factory=lambda: [TestDataclassTuple(2)])
    default_objects: tuple[TestDataclassTuple, ...] = (TestDataclassTuple(3), TestDataclassTuple(4))
    union_parameter: Union[int, str] = "pony"
    tuple_of_union: tuple[Union[int, str], ...] = (1, "pony", 2)
    tuple_of_dataclasses: tuple[Union[TestDataclass, RecursiveTestDataclass], ...] = (TestDataclass(0), RecursiveTestDataclass(1))


@dataclass
class TestDataclassWithStrictTuple:
    strict_tuple: tuple[int, str, TestDataclass]


@dataclass
class TestDataclassWithOptionalParameters:
    number: int
    size: Optional[int]
    colour: Optional[str] = None


@dataclass
class TestDataclassWithUnionParameter:
    number: int
    size: Union[int, tuple[int, int]]

@dataclass
class TestDataclassWithCustomConverter:
    convert: converter


@dataclass
class TestDataclassWithDataclassList:
    dataclass_list: list[TestDataclassSimple]


@dataclass
class TestDataclassWithUnionStartingWithStr:
    options: Union[str, int]


class LowerStr(str):
    def as_data(self):
        return self.lower()

    @classmethod
    def from_data(cls, data: str):
        return cls(data.lower())

@dataclass
class TestDataclassWithCustomClass:
    name: LowerStr


## Dataclasses for class polymorphism testing
@dataclass
class ContainerDataclass:
    dataclass: BaseDataclass


@dataclass
class BaseDataclass:
    first_name: str
    last_name: str


@dataclass
class SubDataclassA(BaseDataclass):
    pass


@dataclass
class SubDataclassB(BaseDataclass):
    favourite_number: int


@dataclass
class SubDataclassAsTuple(BaseDataclass, DataAsTuple):
    pass


@dataclass
class BaseDataclassWithDefault:
    id: int = 100


@dataclass
class SubDataclassAWithDefault(BaseDataclassWithDefault):
    pass


@dataclass
class SubDataclassBWithDefault(BaseDataclassWithDefault):
    max_value: int = 1_000


@dataclass
class SubDataclassWithDefaultAsTuple(BaseDataclassWithDefault, DataAsTuple):
    pass


@dataclass
class ContainerClassWithDefault:
    dataclass: BaseDataclassWithDefault = BaseDataclassWithDefault()


@dataclass
class ContainerClassWithUnionWithBaseClass:
    dataclass: Union[BaseDataclass, str]


## Non-dataclass
class NonDataclass:
    def __init__(self, value: int = None):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.value == other.value

    def __str__(self):
        return f"Number: {self.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value!r})"


@dataclass
class DataclassWithNonDataclass:
    non_dataclass: NonDataclass


@dataclass
class DataclassWithByteArray:
    byte_array: bytearray


class HashableClass:
    def __init__(self, number: int):
        self.number = number

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.number!r})"


@dataclass
class DataclassWithSetsOfDataclasses:
    class_set: set[HashableClass]
    class_frozenset: frozenset[HashableClass]


class NonHashableClass:
    def __init__(self, items: list):
        self.items = items

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.items == other.items

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items!r})"


@dataclass
class DataclassWithListsOfNonDataclasses:
    class_list: list[NonHashableClass]
    class_tuple: tuple[NonHashableClass, NonHashableClass]


@dataclass
class DataclassWithDictsOfNonDataclasses:
    class_dict: dict[str, NonHashableClass]


class SubClassOfNonHashableClass(NonHashableClass): ...


@dataclass
class DataclassWithSubClassOfNonDataclass:
    non_dataclass: NonHashableClass
    sub_non_dataclass: SubClassOfNonHashableClass


@dataclass
class DataclassOfPrimitives:
    string: str
    number: int
    a_bool: bool
    a_float: float
    some_bytes: bytes
    byte_array: bytearray
    a_list: list
    a_tuple: tuple
    a_dict: dict
    a_set: set
    frozen_set: frozenset
    optional_str: Optional[str]


@dataclass
class DataclassConverterTestAsTuple(DataAsTuple):
    number: int
    non_dataclass: NonHashableClass
    class_list: list[NonHashableClass]
    class_set: set[HashableClass]


## Dictionary key conversions
@dataclass(frozen=True)
class FrozenDataclass:
    numbers: tuple[int, ...]


@dataclass
class DataclassWithDataclassAsDictKeys:
    frozen_dataclass_dict: dict[FrozenDataclass, FrozenDataclass]


@dataclass(frozen=True)
class FrozenDataclassWithFrozenDataclass:
    numbers: tuple[int, ...]
    more_numbers: FrozenDataclass


@dataclass
class DataclassWithRecursiveDataclassAsDictKeys:
    frozen_dataclass_dict: dict[FrozenDataclassWithFrozenDataclass, FrozenDataclassWithFrozenDataclass]


@dataclass
class DataclassWithClassAsDictKeys:
    class_dict: dict[HashableClass, NonHashableClass]


class SubclassOfHashableClass(HashableClass): ...


@dataclass
class DataclassWithSubclassAsDictKeys:
    subclass_dict: dict[SubclassOfHashableClass, SubClassOfNonHashableClass]


## Misc
@dataclass
class DataclassWithSets:
    a_set: set[Union[int, str]]
    frozen_set: frozenset[float]


class TestEnum(Enum):
    A = auto()
    B = auto()
    C = auto()


@dataclass
class DataclassWithEnum:
    enums: list[TestEnum]


class TestIntEnum(IntEnum):
    ZERO = 0
    ONE = auto()
    TWO = auto()


@dataclass
class DataclassWithIntEnum:
    int_enums: set[TestIntEnum]


@dataclass
class DataclassWithComplexTypesAsDictKeys:
    complex_dict_a: dict[tuple[HashableClass, FrozenDataclass, tuple[int, Union[TestEnum, HashableClass]]], TestIntEnum]
    complex_dict_b: dict[Optional[Union[TestIntEnum, FrozenDataclassWithFrozenDataclass]], set[Union[TestIntEnum, TestEnum, HashableClass]]]
    complex_dict_c: dict[tuple[FrozenDataclassWithFrozenDataclass, ...], Optional[Union[bytes, frozenset, NonDataclass]]]
