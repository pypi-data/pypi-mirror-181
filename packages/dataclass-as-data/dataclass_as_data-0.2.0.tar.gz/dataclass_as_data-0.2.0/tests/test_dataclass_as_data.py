from __future__ import annotations

import unittest
from typing import Type
from unittest.mock import Mock, seal

from .test_dataclasses import *

from dataclass_as_data import as_data, as_dict, as_tuple, from_data, from_dict, from_tuple, default_converter


class TestAsData(unittest.TestCase):
    def test_as_data(self):
        obj = TestDataclass(6)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0
        })

    def test_as_dict(self):
        obj = TestDataclass(6)

        data = as_dict(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0
        })

    def test_as_tuple(self):
        obj = TestDataclass(6)

        data = as_tuple(obj)

        self.assertTupleEqual(data, (6, "ponies!", 6.0))

    def test_as_data_tuple_dataclass(self):
        obj = TestDataclassTuple(6)

        data = as_data(obj)

        self.assertTupleEqual(data, (6, "ponies!", 6.0))

    def test_recursive_as_data(self):
        obj = RecursiveTestDataclass(6)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

    def test_recursive_as_dict(self):
        obj = RecursiveTestDataclass(6)

        data = as_dict(obj)

        self.assertDictEqual(data, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

    def test_recursive_as_tuple(self):
        obj = RecursiveTestDataclass(6)

        data = as_tuple(obj)

        self.assertTupleEqual(data, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            (1, "ponies!", 6.0)
        ))

    def test_recursive_as_data_tuple_dataclass(self):
        obj = RecursiveTestDataclassTuple(6)

        data = as_data(obj)

        self.assertTupleEqual(data, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0
            },
            (1, "ponies!", 6.0)
        ))

    def test_recursive_as_data_with_containers(self):
        dict_of_test_dataclasses = {
            'a': TestDataclass(0),
            'b': TestDataclass(1)
        }
        obj = RecursiveTestDataClassWithContainers([1, 2, 3], dict_of_test_dataclasses)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'numbers': [1, 2, 3],
            'objects': {
                'a': {
                    'number': 0,
                    'string': "ponies!",
                    'decimal': 6.0
                },
                'b': {
                    'number': 1,
                    'string': "ponies!",
                    'decimal': 6.0
                },
            },
            'extra_objects': [(2, "ponies!", 6.0)],
            'default_objects': ((3, "ponies!", 6.0), (4, "ponies!", 6.0)),
            'union_parameter': "pony",
            'tuple_of_union': (1, "pony", 2),
            'tuple_of_dataclasses':
                ({
                     'number': 0,
                     'string': "ponies!",
                     'decimal': 6.0
                 },
                 {
                     'number': 1,
                     'string': "ponies!",
                     'decimal': 6.0,
                     'test_dataclass': {
                         'number': 0,
                         'string': "ponies!",
                         'decimal': 6.0
                     },
                     'test_dataclass_tuple': (1, "ponies!", 6.0)
                 })
        })

    def test_as_data_with_optional_parameters(self):
        # Test 1
        obj = TestDataclassWithOptionalParameters(159, 21)

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 159,
            'size': 21,
            'colour': None,
        })

        # Test 2
        obj = TestDataclassWithOptionalParameters(159, None, "red")

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 159,
            'size': None,
            'colour': "red",
        })

    def test_as_tuple_with_optional_parameters(self):
        # Test 1
        obj = TestDataclassWithOptionalParameters(159, 21)

        data = as_tuple(obj)

        self.assertEqual(data, (159, 21, None))

        # Test 2
        obj = TestDataclassWithOptionalParameters(159, None, "red")

        data = as_tuple(obj)

        self.assertEqual(data, (159, None, "red"))

    def test_as_data_with_union_parameter(self):
        # Test 1
        obj = TestDataclassWithUnionParameter(789, 13)

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 789,
            'size': 13,
        })

        # Test 2
        obj = TestDataclassWithUnionParameter(789, (3, 3))

        data = as_data(obj)

        self.assertEqual(data, {
            'number': 789,
            'size': (3, 3),
        })

    def test_as_tuple_with_union_parameter(self):
        # Test 1
        obj = TestDataclassWithUnionParameter(789, 13)

        data = as_tuple(obj)

        self.assertEqual(data, (789, 13))

        # Test 2
        obj = TestDataclassWithUnionParameter(789, (3, 3))

        data = as_tuple(obj)

        self.assertEqual(data, (789, (3, 3)))

    ## Tests with class polymorphism
    def test_as_data_with_subclass_member_correctly_adds_type_to_dict(self):
        obj = ContainerDataclass(SubDataclassA("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Sigmath",
                'last_name': "Bits",
            }
        })

    def test_as_data_with_subclass_member_as_tuple_correctly_adds_type_to_tuple(self):
        obj = ContainerDataclass(SubDataclassAsTuple("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': ("Sigmath", "Bits", '__type', "SubDataclassAsTuple")
        })

    def test_as_data_with_base_class_member_doesnt_add_type_to_dict(self):
        obj = ContainerDataclass(BaseDataclass("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                'first_name': "Sigmath",
                'last_name': "Bits",
            }
        })

    def test_as_data_with_subclass_member_with_default_correctly_adds_type_to_dict(self):
        # Test 1
        obj = ContainerClassWithDefault(SubDataclassAWithDefault())

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassAWithDefault",
                'id': 100,
            }
        })

        # Test 2
        obj = ContainerClassWithDefault(SubDataclassBWithDefault())

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassBWithDefault",
                'id': 100,
                'max_value': 1_000,
            }
        })

    def test_as_data_with_subclass_member_as_tuple_with_default_correctly_adds_type_to_dict(self):
        obj = ContainerClassWithDefault(SubDataclassWithDefaultAsTuple())

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': (100, '__type', "SubDataclassWithDefaultAsTuple")
        })

    def test_as_data_with_union_with_subclass_member_correctly_adds_type_to_dict(self):
        obj = ContainerClassWithUnionWithBaseClass(SubDataclassA("Sigmath", "Bits"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Sigmath",
                'last_name': "Bits",
            }
        })

    ## Non-dataclass type conversion
    def test_as_data_with_non_dataclass_in_dataclass_is_not_converted(self):
        obj = DataclassWithNonDataclass(NonDataclass(6))

        data = as_data(obj)

        self.assertEqual(data, {
            'non_dataclass': NonDataclass(6),
        })

    def test_as_data_with_non_dataclass_in_dataclass_is_converted_with_str_as_converter(self):
        obj = DataclassWithNonDataclass(NonDataclass(6))

        data = as_data(obj, converters={default_converter: str})

        self.assertEqual(data, {
            'non_dataclass': "Number: 6",
        })

    def test_as_data_with_non_dataclass_is_converted_with_converter(self):
        obj = NonDataclass(7)

        def non_dataclass_converted(non_dataclass: NonDataclass) -> int:
            return non_dataclass.value

        data = as_data(obj, converters={NonDataclass: non_dataclass_converted})

        self.assertEqual(data, 7)

    def test_as_data_with_non_dataclass_in_dataclass_is_converted_with_converter(self):
        obj = DataclassWithNonDataclass(NonDataclass(7))

        def non_dataclass_converter(non_dataclass: NonDataclass) -> int:
            return non_dataclass.value

        data = as_data(obj, converters={NonDataclass: non_dataclass_converter})

        self.assertEqual(data, {
            'non_dataclass': 7,
        })

    def test_as_data_with_non_dataclass_is_converted_with_default_converter(self):
        obj = DataclassWithNonDataclass(NonDataclass(888))

        def non_dataclass_converter(non_dataclass: NonDataclass) -> int:
            return non_dataclass.value

        data = as_data(obj, converters={default_converter: non_dataclass_converter})

        self.assertEqual(data, {
            'non_dataclass': 888,
        })

    def test_as_data_with_bytearray_is_converted_with_converter(self):
        obj = DataclassWithByteArray(bytearray(b'pony!'))

        def bytearray_converter(byte_array: bytearray) -> str:
            return byte_array.decode('utf-8')

        data = as_data(obj, converters={bytearray: bytearray_converter})

        self.assertEqual(data, {
            'byte_array': "pony!",
        })

    def test_as_data_with_sets_of_hashable_non_dataclasses_is_converted_with_converter(self):
        obj = DataclassWithSetsOfDataclasses(
            {HashableClass(2), HashableClass(3)},
            frozenset({HashableClass(3), HashableClass(4)})
        )

        def non_dataclass_as_int(_obj: HashableClass) -> int:
            return _obj.number

        data = as_data(obj, converters={HashableClass: non_dataclass_as_int})

        self.assertDictEqual(data, {
            'class_set': {2, 3},
            'class_frozenset': frozenset({3, 4}),
        })

    def test_as_data_with_lists_of_unhasable_non_dataclasses_is_converted_with_converter(self):
        obj = DataclassWithListsOfNonDataclasses(
            [NonHashableClass([1, 2, 3]), NonHashableClass([1, 2]), NonHashableClass([1])],
            (NonHashableClass([1, 2, 3, 4]), NonHashableClass([1, 2, 3, 4, 5]))
        )

        def non_dataclass_as_int(_obj: NonHashableClass) -> int:
            return len(_obj.items)

        data = as_data(obj, converters={NonHashableClass: non_dataclass_as_int})

        self.assertDictEqual(data, {
            'class_list': [3, 2, 1],
            'class_tuple': (4, 5),
        })

    def test_as_data_with_dicts_of_non_dataclasses_is_converted_with_converter(self):
        obj = DataclassWithDictsOfNonDataclasses({
            '3 items': NonHashableClass([1, 2, 3]),
            '2 items': NonHashableClass([1, 2]),
            '1 item': NonHashableClass([1]),
        })

        def non_dataclass_as_int(_obj: NonHashableClass) -> int:
            return len(_obj.items)

        data = as_data(obj, converters={NonHashableClass: non_dataclass_as_int})

        self.assertDictEqual(data, {
            'class_dict':{
                '3 items': 3,
                '2 items': 2,
                '1 item': 1,
            }
        })

    def test_as_data_with_sub_class_of_non_dataclass_is_converted_with_base_converter_when_kwarg_specified(self):
        obj = DataclassWithSubClassOfNonDataclass(
            NonHashableClass([1, 2, 3]),
            SubClassOfNonHashableClass([6, 5, 4, 3, 2, 1])
        )

        def non_dataclass_as_int(_obj: NonHashableClass, *, cls: type) -> int:
            return len(_obj.items)

        data = as_data(obj, converters={NonHashableClass: non_dataclass_as_int})

        self.assertDictEqual(data, {
            'non_dataclass': 3,
            'sub_non_dataclass': 6,
        })

    def test_as_data_with_sub_class_of_non_dataclass_is_not_converted_with_base_converter_when_kwarg_not_specified(self):
        obj = DataclassWithSubClassOfNonDataclass(
            NonHashableClass([1, 2, 3]),
            SubClassOfNonHashableClass([6, 5, 4, 3, 2, 1])
        )

        def non_dataclass_as_int(_obj: NonHashableClass) -> int:
            return len(_obj.items)

        data = as_data(obj, converters={NonHashableClass: non_dataclass_as_int})

        self.assertDictEqual(data, {
            'non_dataclass': 3,
            'sub_non_dataclass': SubClassOfNonHashableClass([6, 5, 4, 3, 2, 1]),
        })

    def test_as_data_with_sub_class_of_non_dataclass_is_converted_with_overriden_converter(self):
        obj = DataclassWithSubClassOfNonDataclass(
            NonHashableClass([1, 2, 3]),
            SubClassOfNonHashableClass([6, 5, 4, 3, 2, 1])
        )

        def non_dataclass_as_int(_obj: NonHashableClass) -> int:
            return len(_obj.items)

        def non_dataclass_as_str(_obj: NonHashableClass) -> str:
            return ", ".join(str(item) for item in _obj.items)

        data = as_data(obj, converters={
            NonHashableClass: non_dataclass_as_int,
            SubClassOfNonHashableClass: non_dataclass_as_str
        })

        self.assertDictEqual(data, {
            'non_dataclass': 3,
            'sub_non_dataclass': "6, 5, 4, 3, 2, 1",
        })

    def test_as_data_primitives_not_affected_by_default_converter(self):
        obj = DataclassOfPrimitives(
            "pony", 6, True, 3.142, b'pony', bytearray(b'pony'), ["a", "b", "c"], (1, 2), {'a': 1, 'b': 2},
            {"pony", "town", "pony"}, frozenset({"sixty", "sigsty"}), None,
        )

        data = as_data(obj, converters={default_converter: repr})

        self.assertDictEqual(data, {
            'string': "pony",
            'number': 6,
            'a_bool': True,
            'a_float': 3.142,
            'some_bytes': b'pony',
            'byte_array': bytearray(b'pony'),
            'a_list': ["a", "b", "c"],
            'a_tuple': (1, 2),
            'a_dict': {'a': 1, 'b': 2},
            'a_set': {"pony", "town", "pony"},
            'frozen_set': frozenset({"sixty", "sigsty"}),
            'optional_str': None,
        })

    def test_as_data_tuple_data_is_converter_with_converter(self):
        obj = DataclassConverterTestAsTuple(
            6,
            NonHashableClass([1, 2, 3]),
            [NonHashableClass([1, 2]), NonHashableClass([1, 2, 3, 3])],
            {HashableClass(7), HashableClass(4), HashableClass(11)}
        )

        def non_hashable_class_converter(_obj: NonHashableClass) -> int:
            return len(_obj.items)

        def hashable_class_converter(_obj: HashableClass) -> int:
            return _obj.number

        data = as_data(
            obj,
            converters={NonHashableClass: non_hashable_class_converter, HashableClass: hashable_class_converter}
        )

        self.assertTupleEqual(data, (
            6,
            3,
            [2, 4],
            {7, 4, 11},
        ))

    def test_as_dict_raises_type_error_for_non_dataclasses(self):
        obj = NonHashableClass([1, 2, 3])

        with self.assertRaises(TypeError):
            _data = as_dict(obj)

    def test_as_tuple_raises_type_error_for_non_dataclasses(self):
        obj = NonHashableClass([1, 2, 3])

        with self.assertRaises(TypeError):
            _data = as_tuple(obj)

    ## Dictionary key conversions Tests
    def test_as_data_with_dataclasses_as_dict_keys(self):
        obj = DataclassWithDataclassAsDictKeys({
            FrozenDataclass((1, 2, 3)): FrozenDataclass((4, 5, 6)),
            FrozenDataclass((6,)): FrozenDataclass((0,)),
            FrozenDataclass((10, 11)): FrozenDataclass((3, 3)),
        })

        data = as_data(obj)

        self.assertDictEqual(data, {
            'frozen_dataclass_dict': {
                ((1, 2, 3),): {
                    'numbers': (4, 5, 6)
                },
                ((6,),): {
                    'numbers': (0,)
                },
                ((10, 11),): {
                    'numbers': (3, 3)
                },
            }
        })

    def test_as_data_with_recursive_dataclasses_as_dict_keys(self):
        obj = DataclassWithRecursiveDataclassAsDictKeys({
            FrozenDataclassWithFrozenDataclass((1, 2, 3), FrozenDataclass((1, 2, 3))):
                FrozenDataclassWithFrozenDataclass((4, 5, 6), FrozenDataclass((4, 5, 6))),
            FrozenDataclassWithFrozenDataclass((0,), FrozenDataclass((6, 6, 6))):
                FrozenDataclassWithFrozenDataclass((1,), FrozenDataclass((6, 1, 6))),
        })

        data = as_data(obj)

        self.assertDictEqual(data, {
            'frozen_dataclass_dict': {
                ((1, 2, 3), ((1, 2, 3),)): {
                    'numbers': (4, 5, 6),
                    'more_numbers': {
                        'numbers': (4, 5, 6),
                    }
                },
                ((0,), ((6, 6, 6),)): {
                    'numbers': (1,),
                    'more_numbers': {
                        'numbers': (6, 1, 6),
                    }
                },
            }
        })

    def test_as_data_with_non_dataclass_as_dict_keys_uses_converter(self):
        obj = DataclassWithClassAsDictKeys({
            HashableClass(6): NonHashableClass([1, 2, 3]),
            HashableClass(7): NonHashableClass([4, 7, 11]),
        })

        def hashable_class_to_int(_obj: HashableClass) -> int:
            return _obj.number

        def nonhashable_class_to_str(_obj: NonHashableClass) -> str:
            return ", ".join(str(value) for value in _obj.items)

        data = as_data(
            obj,
            converters={HashableClass: hashable_class_to_int,
                        NonHashableClass: nonhashable_class_to_str}
        )

        self.assertDictEqual(data, {
            'class_dict': {
                6: "1, 2, 3",
                7: "4, 7, 11",
            }
        })

    def test_as_tuple_with_dataclasses_as_dict_keys(self):
        obj = DataclassWithDataclassAsDictKeys({
            FrozenDataclass((1, 2, 3)): FrozenDataclass((4, 5, 6)),
            FrozenDataclass((6,)): FrozenDataclass((0,)),
            FrozenDataclass((10, 11)): FrozenDataclass((3, 3)),
        })

        data = as_tuple(obj)

        self.assertTupleEqual(data, (
            {
                ((1, 2, 3),): {
                    'numbers': (4, 5, 6)
                },
                ((6,),): {
                    'numbers': (0,)
                },
                ((10, 11),): {
                    'numbers': (3, 3)
                },
            },
        ))

    def test_as_data_with_sub_class_of_non_dataclass_as_dict_keys_is_converted_with_base_converter_when_kwarg_specified(self):
        obj = DataclassWithSubclassAsDictKeys({
            SubclassOfHashableClass(6): SubClassOfNonHashableClass([1, 2, 3]),
            SubclassOfHashableClass(7): SubClassOfNonHashableClass([4, 7, 11]),
        })

        def hashable_class_to_int(_obj: HashableClass, *, _cls) -> int:
            return _obj.number

        def nonhashable_class_to_str(_obj: NonHashableClass, *, _cls) -> str:
            return ", ".join(str(value) for value in _obj.items)

        data = as_data(
            obj,
            converters={HashableClass: hashable_class_to_int,
                        NonHashableClass: nonhashable_class_to_str}
        )

        self.assertDictEqual(data, {
            'subclass_dict': {
                6: "1, 2, 3",
                7: "4, 7, 11",
            }
        })

    def test_as_data_with_sub_class_of_non_dataclass_as_dict_keys_is_not_converted_with_base_converter_when_kwarg_not_specified(self):
        obj = DataclassWithSubclassAsDictKeys({
            SubclassOfHashableClass(6): SubClassOfNonHashableClass([1, 2, 3]),
            SubclassOfHashableClass(7): SubClassOfNonHashableClass([4, 7, 11]),
        })

        def hashable_class_to_int(_obj: HashableClass) -> int:
            return _obj.number

        def nonhashable_class_to_str(_obj: NonHashableClass) -> str:
            return ", ".join(str(value) for value in _obj.items)

        data = as_data(
            obj,
            converters={HashableClass: hashable_class_to_int,
                        NonHashableClass: nonhashable_class_to_str}
        )

        self.assertDictEqual(data, {
            'subclass_dict': {
                SubclassOfHashableClass(6): SubClassOfNonHashableClass([1, 2, 3]),
                SubclassOfHashableClass(7): SubClassOfNonHashableClass([4, 7, 11]),
            }
        })

    ## Remaining Tests
    def test_as_data_with_union_with_subclass_passing_non_subclass_member_correctly_doesnt_add_type(self):
        obj = ContainerClassWithUnionWithBaseClass("Sigmath Bits")

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': "Sigmath Bits"
        })

    def test_as_data_with_union_with_subclass_member_as_tuple_correctly_adds_type_to_dict(self):
        obj = ContainerClassWithUnionWithBaseClass(SubDataclassAsTuple("Rainbow", "Dash"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass': ("Rainbow", "Dash", '__type', "SubDataclassAsTuple")
        })

    def test_as_data_functions_correctly_with_custom_converter(self):
        obj = TestDataclassWithCustomConverter(10)

        data = as_data(obj)

        self.assertDictEqual(data, {
            'convert': 10,
        })

    def test_as_data_with_dataclass_list_correctly_doesnt_add_type_to_dict(self):
        obj = TestDataclassWithDataclassList([TestDataclassSimple(6), TestDataclassSimple(7)])

        data = as_data(obj)

        self.assertDictEqual(data, {
            'dataclass_list': [
                {'number': 6},
                {'number': 7}
            ]
        })

    def test_as_data_with_custom_class_defining_as_data(self):
        obj = TestDataclassWithCustomClass(LowerStr("Derpy!"))

        data = as_data(obj)

        self.assertDictEqual(data, {
            'name': "derpy!"
        })

    def test_as_data_with_sets(self):
        obj = DataclassWithSets({1, 2, 3, "pony"}, frozenset({1.2, 3.4, 7.0}))

        data = as_data(obj)

        self.assertEqual(data, {
            'a_set': {1, 2, 3, "pony"},
            'frozen_set': frozenset({1.2, 3.4, 7}),
        })

    def test_as_data_doesnt_converts_enums_by_default(self):
        obj = DataclassWithEnum([TestEnum.A, TestEnum.B, TestEnum.C])

        data = as_data(obj)

        self.assertDictEqual(data, {
            'enums': [
                TestEnum.A,
                TestEnum.B,
                TestEnum.C,
            ]
        })


class TestFromData(unittest.TestCase):
    def test_from_data(self):
        obj = from_data(TestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'WRONG': "OOPS"
        })

        self.assertEqual(obj, TestDataclass(6))

    def test_from_dict(self):
        obj = from_dict(TestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            'WRONG': "OOPS"
        })

        self.assertEqual(obj, TestDataclass(6))

    def test_from_tuple(self):
        obj = from_tuple(TestDataclass, (6, "ponies!", 6.0))

        self.assertEqual(obj, TestDataclass(6))

    def test_from_tuple_using_from_data(self):
        obj = from_data(TestDataclass, (6, "ponies!", 6.0))

        self.assertEqual(obj, TestDataclass(6))

    def test_from_data_tuple_dataclass(self):
        obj = from_data(TestDataclassTuple, (6, "ponies!", 6.0))

        self.assertEqual(obj, TestDataclassTuple(6))

    def test_recursive_from_data(self):
        obj = from_data(RecursiveTestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            "WRONG": "OOPS!",
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

        self.assertEqual(obj, RecursiveTestDataclass(6))

    def test_recursive_from_dict(self):
        obj = from_dict(RecursiveTestDataclass, {
            'number': 6,
            'string': "ponies!",
            'decimal': 6.0,
            "WRONG": "OOPS!",
            'test_dataclass': {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            'test_dataclass_tuple': (1, "ponies!", 6.0)
        })

        self.assertEqual(obj, RecursiveTestDataclass(6))

    def test_recursive_from_tuple(self):
        obj = from_tuple(RecursiveTestDataclass, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            (1, "ponies!", 6.0)
        ))

        self.assertEqual(obj, RecursiveTestDataclass(6))

    def test_recursive_from_data_tuple_dataclass(self):
        obj = from_data(RecursiveTestDataclassTuple, (
            6, "ponies!", 6.0,
            {
                'number': 0,
                'string': "ponies!",
                'decimal': 6.0,
                "WRONG": "OOPS!",
            },
            (1, "ponies!", 6.0)
        ))

        self.assertEqual(obj, RecursiveTestDataclassTuple(6))

    def test_recursive_from_data_with_containers(self):
        obj_from_data = from_data(RecursiveTestDataClassWithContainers, {
            'numbers': [1, 2, 3],
            'objects': {
                'a': {
                    'number': 0,
                    'string': "ponies!",
                    'decimal': 6.0
                },
                'b': {
                    'number': 1,
                    'string': "ponies!",
                    'decimal': 6.0
                },
            },
            'extra_objects': [(2, "ponies!", 6.0)],
            'default_objects': ((3, "ponies!", 6.0), (4, "ponies!", 6.0)),
            'optional_parameter': 10_000,
        })

        dict_of_test_dataclasses = {
            'a': TestDataclass(0),
            'b': TestDataclass(1)
        }
        obj = RecursiveTestDataClassWithContainers([1, 2, 3], dict_of_test_dataclasses)

        self.assertEqual(obj_from_data, obj)

    def test_strict_tuple_converted_correctly(self):
        obj = from_data(TestDataclassWithStrictTuple, {
            'strict_tuple': (6, "pony", {'number': 9})
        })

        self.assertEqual(obj, TestDataclassWithStrictTuple((6, "pony", TestDataclass(9))))

    def test_strict_tuple_conversion_raises_type_error_with_incorrect_element_count(self):
        # Test 1
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclassWithStrictTuple, {
                'strict_tuple': (6, "pony", {'number': 9}, 10)
            })

        # Test 2
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclassWithStrictTuple, {
                'strict_tuple': (6, "pony")
            })

    def test_from_data_with_optional_parameters(self):
        # Test 1
        obj = from_data(TestDataclassWithOptionalParameters, {
            'number': 354,
            'size': 12,
        })

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, 12))

        # Test 2
        obj = from_data(TestDataclassWithOptionalParameters, {
            'number': 354,
            'size': None,
        })

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, None))

        # Test 3
        obj = from_data(TestDataclassWithOptionalParameters, {
            'number': 354,
            'size': None,
            'colour': "red",
        })

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, None, "red"))

    def test_from_tuple_with_optional_parameters(self):
        obj = from_tuple(TestDataclassWithOptionalParameters, (354, None, "red"))

        self.assertEqual(obj, TestDataclassWithOptionalParameters(354, None, "red"))

    def test_from_data_with_union_parameter(self):
        # Test 1
        obj = from_data(TestDataclassWithUnionParameter, {
            'number': 354,
            'size': 12,
        })

        self.assertEqual(obj, TestDataclassWithUnionParameter(354, 12))

        # Test 2
        obj = from_data(TestDataclassWithUnionParameter, {
            'number': 354,
            'size': (2, 5),
        })

        self.assertEqual(obj, TestDataclassWithUnionParameter(354, (2, 5)))

    def test_from_tuple_with_union_parameter(self):
        obj = from_data(TestDataclassWithUnionParameter, (354, (2, 5)))

        self.assertEqual(obj, TestDataclassWithUnionParameter(354, (2, 5)))

    def test_from_data_with_union_parameter_raises_type_error_if_doesnt_match_any_union_type(self):
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclassWithUnionParameter, {
                'number': 354,
                'size': "asd",
            })

    def test_from_data_converts_str_to_int_if_possible(self):
        obj = from_data(TestDataclass, {
            'number': "666",
        })

        self.assertEqual(obj, TestDataclass(666))

    def test_from_data_raises_type_error_if_conversion_from_str_to_int_not_possible(self):
        with self.assertRaises(TypeError):
            _obj = from_data(TestDataclass, {
                'number': "pony"
            })

    def test_from_data_tuple_data_is_converter_with_converter(self):
        data = (
            6,
            "1, 2, 3",
            ["1, 2", "1, 2, 3, 3"],
            {7, 4, 11},
        )
        def non_hashable_class_converter(string: str) -> NonHashableClass:
            return NonHashableClass([int(value) for value in string.split(", ")])

        def hashable_class_converter(value: int) -> HashableClass:
            return HashableClass(value)

        obj = from_data(
            DataclassConverterTestAsTuple,
            data,
            converters={NonHashableClass: non_hashable_class_converter, HashableClass: hashable_class_converter}
        )

        self.assertEqual(obj, DataclassConverterTestAsTuple(
            6,
            NonHashableClass([1, 2, 3]),
            [NonHashableClass([1, 2]), NonHashableClass([1, 2, 3, 3])],
            {HashableClass(7), HashableClass(4), HashableClass(11)}
        ))

    def test_from_data_raises_type_error_for_non_dataclasses(self):
        data = {
            'items': [1, 2, 3]
        }

        with self.assertRaises(TypeError):
            _data = from_data(NonHashableClass, data)

    def test_from_dict_raises_type_error_for_non_dataclasses(self):
        data = {
            'items': [1, 2, 3]
        }

        with self.assertRaises(TypeError):
            _data = from_dict(NonHashableClass, data)

    def test_from_tuple_raises_type_error_for_non_dataclasses(self):
        data = ([1, 2, 3],)

        with self.assertRaises(TypeError):
            _data = from_tuple(NonHashableClass, data)

    ## Tests with class polymorphism
    def test_from_data_with_subclass_member_uses_explicit_type(self):
        obj = from_data(ContainerDataclass, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Rainbow",
                'last_name': "Dash",
            }
        })

        self.assertEqual(obj, ContainerDataclass(SubDataclassA("Rainbow", "Dash")))

    def test_from_data_with_subclass_member_with_different_parameters_converts_incorrectly_without_explicit_type(self):
        obj = from_data(ContainerDataclass, {
            'dataclass': {
                'first_name': "Rainbow",
                'last_name': "Dash",
                'favourite_number': 6,
            }
        })

        self.assertNotIsInstance(obj.dataclass, SubDataclassB)

    def test_from_data_with_subclass_member_as_tuple_uses_explicit_type(self):
        obj = from_data(ContainerDataclass, {
            'dataclass': ("Rainbow", "Dash", '__type', "SubDataclassAsTuple")
        })

        self.assertEqual(obj, ContainerDataclass(SubDataclassAsTuple("Rainbow", "Dash")))

    def test_from_data_with_subclass_member_with_default_uses_explicit_type(self):
        # Test 1
        obj = from_data(ContainerClassWithDefault, {
            'dataclass': {
                '__type': "SubDataclassAWithDefault"
            }
        })

        self.assertEqual(obj, ContainerClassWithDefault(SubDataclassAWithDefault()))

        # Test 2
        obj = from_data(ContainerClassWithDefault, {
            'dataclass': {
                '__type': "SubDataclassBWithDefault"
            }
        })

        self.assertEqual(obj, ContainerClassWithDefault(SubDataclassBWithDefault()))

    def test_from_data_with_subclass_member_as_tuple_with_default_uses_explicit_type(self):
        obj = from_data(ContainerClassWithDefault, {
            'dataclass': ('__type', "SubDataclassWithDefaultAsTuple")
        })

        self.assertEqual(obj, ContainerClassWithDefault(SubDataclassWithDefaultAsTuple()))

    def test_from_data_with_union_with_subclass_member_uses_explicit_type(self):
        obj = from_data(ContainerClassWithUnionWithBaseClass, {
            'dataclass': {
                '__type': "SubDataclassA",
                'first_name': "Rainbow",
                'last_name': "Dash",
            }
        })

        self.assertEqual(obj, ContainerClassWithUnionWithBaseClass(SubDataclassA("Rainbow", "Dash")))

    def test_from_tuple_with_union_with_subclass_member_uses_explicit_type(self):
        obj = from_data(ContainerClassWithUnionWithBaseClass, {
            'dataclass': ("Rainbow", "Dash", '__type', "SubDataclassA")
        })

        self.assertEqual(obj, ContainerClassWithUnionWithBaseClass(SubDataclassA("Rainbow", "Dash")))

    def test_from_data_with_non_dataclass_calls_constructor_by_default(self):
        obj = from_data(DataclassWithNonDataclass, {'non_dataclass': 123})

        self.assertEqual(obj, DataclassWithNonDataclass(NonDataclass(123)))

    def test_from_data_with_non_dataclass_is_constructed_with_converter(self):
        def non_dataclass_from_string(string: str) -> NonDataclass:
            return NonDataclass(len(string))

        obj = from_data(
            DataclassWithNonDataclass,
            {'non_dataclass': "ponies"},
            converters={NonDataclass: non_dataclass_from_string},
        )

        self.assertEqual(obj, DataclassWithNonDataclass(NonDataclass(6)))

    def test_from_data_with_non_dataclass_is_constructed_with_default_converter(self):
        def non_dataclass_from_string(string: str) -> NonDataclass:
            return NonDataclass(len(string))

        obj = from_data(
            DataclassWithNonDataclass,
            {'non_dataclass': "ponies"},
            converters={default_converter: non_dataclass_from_string},
        )

        self.assertEqual(obj, DataclassWithNonDataclass(NonDataclass(6)))

    def test_from_data_with_sets_of_hashable_non_dataclasses_is_converted_with_converter(self):
        data = {
            'class_set': {2, 3},
            'class_frozenset': frozenset({3, 4}),
        }

        def non_dataclass_from_int(number: int) -> HashableClass:
            return HashableClass(number)

        obj = from_data(DataclassWithSetsOfDataclasses, data, converters={HashableClass: non_dataclass_from_int})

        self.assertEqual(
            obj,
            DataclassWithSetsOfDataclasses(
                {HashableClass(2), HashableClass(3)},
                frozenset({HashableClass(3), HashableClass(4)})
            )
        )

    def test_from_data_with_lists_of_unhasable_non_dataclasses_is_converted_with_converter(self):
        data = {
            'class_list': ["1, 2, 3", "1, 2", "1"],
            'class_tuple': ("1, 2, 3, 4", "1, 2, 3, 4, 5"),
        }

        def non_dataclass_from_str(string: str) -> NonHashableClass:
            return NonHashableClass([int(value) for value in string.split(", ")])

        obj = from_data(DataclassWithListsOfNonDataclasses, data, converters={NonHashableClass: non_dataclass_from_str})

        self.assertEqual(
            obj,
            DataclassWithListsOfNonDataclasses(
                [NonHashableClass([1, 2, 3]), NonHashableClass([1, 2]), NonHashableClass([1])],
                (NonHashableClass([1, 2, 3, 4]), NonHashableClass([1, 2, 3, 4, 5]))
            )
        )

    def test_from_data_with_dicts_of_non_dataclasses_is_converted_with_converter(self):
        data = {
            'class_dict':{
                '3 items': "1, 2, 3",
                '2 items': "1, 2",
                '1 item': "1",
            }
        }

        def non_dataclass_from_str(string: str) -> NonHashableClass:
            return NonHashableClass([int(value) for value in string.split(", ")])

        obj = from_data(DataclassWithDictsOfNonDataclasses, data, converters={NonHashableClass: non_dataclass_from_str})

        self.assertEqual(
            obj,
            DataclassWithDictsOfNonDataclasses({
                '3 items': NonHashableClass([1, 2, 3]),
                '2 items': NonHashableClass([1, 2]),
                '1 item': NonHashableClass([1]),
            })
        )

    def test_from_data_with_sub_class_of_non_dataclass_is_converted_with_base_converter_when_kwarg_specified(self):
        data = {
            'non_dataclass': "1, 2, 3",
            'sub_non_dataclass': "6, 5, 4, 3, 2, 1",
        }

        def non_dataclass_from_str(string: str, *, cls: Type[NonHashableClass]) -> NonHashableClass:
            return cls([int(value) for value in string.split(", ")])

        data = from_data(DataclassWithSubClassOfNonDataclass, data, converters={NonHashableClass: non_dataclass_from_str})

        self.assertEqual(data, DataclassWithSubClassOfNonDataclass(
            NonHashableClass([1, 2, 3]),
            SubClassOfNonHashableClass([6, 5, 4, 3, 2, 1])
        ))

    def test_from_data_with_sub_class_of_non_dataclass_is_not_converted_with_base_converter_when_kwarg_not_specified(self):
        data = {
            'non_dataclass': "1, 2, 3",
            'sub_non_dataclass': "6, 5, 4, 3, 2, 1",
        }

        def non_dataclass_from_str(string: str) -> NonHashableClass:
            return NonHashableClass([int(value) for value in string.split(", ")])

        data = from_data(DataclassWithSubClassOfNonDataclass, data, converters={NonHashableClass: non_dataclass_from_str})

        self.assertEqual(data, DataclassWithSubClassOfNonDataclass(
            NonHashableClass([1, 2, 3]),
            SubClassOfNonHashableClass("6, 5, 4, 3, 2, 1"),  # type: ignore
        ))

    def test_from_data_primitives_not_affected_by_default_converter(self):
        data = {
            'string': "pony",
            'number': 6,
            'a_bool': True,
            'a_float': 3.142,
            'some_bytes': b'pony',
            'byte_array': bytearray(b'pony'),
            'a_list': ["a", "b", "c"],
            'a_tuple': (1, 2),
            'a_dict': {'a': 1, 'b': 2},
            'a_set': {"pony", "town", "pony"},
            'frozen_set': frozenset({"sixty", "sigsty"}),
            'optional_str': None,
        }

        obj = from_data(DataclassOfPrimitives, data, converters={default_converter: repr})

        self.assertEqual(obj, DataclassOfPrimitives(
            "pony", 6, True, 3.142, b'pony', bytearray(b'pony'), ["a", "b", "c"], (1, 2), {'a': 1, 'b': 2},
            {"pony", "town"}, frozenset({"sixty", "sigsty"}), None,
        ))

    ## Dictionary key conversions Tests
    def test_from_data_with_dataclasses_as_dict_keys(self):
        data = {
            'frozen_dataclass_dict': {
                ((1, 2, 3),): {
                    'numbers': (4, 5, 6)
                },
                ((6,),): {
                    'numbers': (0,)
                },
                ((10, 11),): {
                    'numbers': (3, 3)
                },
            }
        }

        obj = from_data(DataclassWithDataclassAsDictKeys, data)

        self.assertEqual(obj, DataclassWithDataclassAsDictKeys({
            FrozenDataclass((1, 2, 3)): FrozenDataclass((4, 5, 6)),
            FrozenDataclass((6,)): FrozenDataclass((0,)),
            FrozenDataclass((10, 11)): FrozenDataclass((3, 3)),
        }))

    def test_from_data_with_recursive_dataclasses_as_dict_keys(self):
        data = {
            'frozen_dataclass_dict': {
                ((1, 2, 3), ((1, 2, 3),)): {
                    'numbers': (4, 5, 6),
                    'more_numbers': {
                        'numbers': (4, 5, 6),
                    }
                },
                ((0,), ((6, 6, 6),)): {
                    'numbers': (1,),
                    'more_numbers': {
                        'numbers': (6, 1, 6),
                    }
                },
            }
        }

        obj = from_data(DataclassWithRecursiveDataclassAsDictKeys, data)

        self.assertEqual(obj, DataclassWithRecursiveDataclassAsDictKeys({
            FrozenDataclassWithFrozenDataclass((1, 2, 3), FrozenDataclass((1, 2, 3))):
                FrozenDataclassWithFrozenDataclass((4, 5, 6), FrozenDataclass((4, 5, 6))),
            FrozenDataclassWithFrozenDataclass((0,), FrozenDataclass((6, 6, 6))):
                FrozenDataclassWithFrozenDataclass((1,), FrozenDataclass((6, 1, 6))),
        }))

    def test_from_data_with_non_dataclass_as_dict_keys_uses_converter(self):
        data = {
            'class_dict': {
                6: "1, 2, 3",
                7: "4, 7, 11",
            }
        }

        def int_to_hashable_class(number: int) -> HashableClass:
            return HashableClass(number)

        def str_to_nonhashable_class(string: str) -> NonHashableClass:
            return NonHashableClass([int(value) for value in string.split(", ")])

        obj = from_data(
            DataclassWithClassAsDictKeys,
            data,
            converters={HashableClass: int_to_hashable_class,
                        NonHashableClass: str_to_nonhashable_class}
        )

        self.assertEqual(obj, DataclassWithClassAsDictKeys({
            HashableClass(6): NonHashableClass([1, 2, 3]),
            HashableClass(7): NonHashableClass([4, 7, 11]),
        }))

    def test_from_tuple_with_dataclasses_as_dict_keys(self):
        data = (
            {
                ((1, 2, 3),): {
                    'numbers': (4, 5, 6)
                },
                ((6,),): {
                    'numbers': (0,)
                },
                ((10, 11),): {
                    'numbers': (3, 3)
                },
            },
        )

        obj = from_data(DataclassWithDataclassAsDictKeys, data)

        self.assertEqual(obj, DataclassWithDataclassAsDictKeys({
            FrozenDataclass((1, 2, 3)): FrozenDataclass((4, 5, 6)),
            FrozenDataclass((6,)): FrozenDataclass((0,)),
            FrozenDataclass((10, 11)): FrozenDataclass((3, 3)),
        }))

    def test_from_data_with_sub_class_of_non_dataclass_as_dict_keys_is_converted_with_base_converter_when_kwarg_specified(self):
        data = {
            'subclass_dict': {
                '6': "1, 2, 3",
                '7': "4, 7, 11",
            }
        }

        def str_to_hashable_class(number: str, *, cls) -> HashableClass:
            return cls(int(number))

        def str_to_nonhashable_class(string: str, *, cls) -> NonHashableClass:
            return cls([int(value) for value in string.split(", ")])

        obj = from_data(
            DataclassWithSubclassAsDictKeys,
            data,
            converters={HashableClass: str_to_hashable_class,
                        NonHashableClass: str_to_nonhashable_class}
        )

        self.assertEqual(obj, DataclassWithSubclassAsDictKeys({
            SubclassOfHashableClass(6): SubClassOfNonHashableClass([1, 2, 3]),
            SubclassOfHashableClass(7): SubClassOfNonHashableClass([4, 7, 11]),
        }))

    def test_from_data_with_sub_class_of_non_dataclass_as_dict_keys_is_not_converted_with_base_converter_when_kwarg_not_specified(self):
        data = {
            'subclass_dict': {
                '6': "1, 2, 3",
                '7': "4, 7, 11",
            }
        }

        def str_to_hashable_class(number: str) -> HashableClass:
            return HashableClass(int(number))

        def str_to_nonhashable_class(string: str) -> NonHashableClass:
            return NonHashableClass([int(value) for value in string.split(", ")])

        obj = from_data(
            DataclassWithSubclassAsDictKeys,
            data,
            converters={HashableClass: str_to_hashable_class,
                        NonHashableClass: str_to_nonhashable_class}
        )

        self.assertEqual(obj, DataclassWithSubclassAsDictKeys({
            SubclassOfHashableClass('6'): SubClassOfNonHashableClass("1, 2, 3"),  # type: ignore
            SubclassOfHashableClass('7'): SubClassOfNonHashableClass("4, 7, 11"),  # type: ignore
        }))

    ## Remaining Tests
    def test_from_data_with_custom_converter_is_called(self):
        converter.return_value = 10

        # This is only allowed so long as it's the only use of converter, since `converter` is global
        # (The use of local converters is not supported)
        seal(converter)

        obj = from_data(TestDataclassWithCustomConverter, {'convert': "pony"})

        converter.assert_called_once_with("pony")
        self.assertEqual(obj, TestDataclassWithCustomConverter(10))

    def test_from_data_with_union_starting_with_str_converts_other_types_if_possible(self):
        obj = from_data(TestDataclassWithUnionStartingWithStr, {
            'options': 123,
        })

        self.assertEqual(obj, TestDataclassWithUnionStartingWithStr(123))

    def test_from_data_with_union_starting_with_str_converts_to_str_if_only_possibility(self):
        obj = from_data(TestDataclassWithUnionStartingWithStr, {
            'options': None,
        })

        self.assertEqual(obj, TestDataclassWithUnionStartingWithStr("None"))

    def test_from_data_with_custom_class_defining_from_data(self):
        obj = from_data(TestDataclassWithCustomClass, {
            'name': "Pony!"
        })

        self.assertEqual(obj, TestDataclassWithCustomClass(LowerStr("pony!")))

    def test_from_data_with_sets(self):
        obj = from_data(DataclassWithSets, {
            'a_set': (1, 2, 3, "pony"),
            'frozen_set': (1.2, 3.4, 7),
        })

        self.assertEqual(obj, DataclassWithSets({1, 2, 3, "pony"}, frozenset({1.2, 3.4, 7.0})))

    def test_from_data_converts_ints_to_int_enums_by_default(self):
        data = {
            'int_enums': (0, 1, 2)
        }

        obj = from_data(DataclassWithIntEnum, data)

        self.assertEqual(obj, DataclassWithIntEnum({TestIntEnum.ZERO, TestIntEnum.ONE, TestIntEnum.TWO}))

    def test_from_data_calls_custom_class_init_if_types_dont_match(self):
        data = {
            'non_dataclass': 6
        }

        obj = from_data(DataclassWithNonDataclass, data)

        self.assertEqual(obj, DataclassWithNonDataclass(NonDataclass(6)))

    def test_from_data_doesnt_call_class_init_if_types_match(self):
        data = {
            'non_dataclass': NonDataclass(6)
        }

        obj = from_data(DataclassWithNonDataclass, data)

        self.assertEqual(obj, DataclassWithNonDataclass(NonDataclass(6)))


class TestAsDataFromData(unittest.TestCase):
    def test_dataclass_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = TestDataclass(123)

        data = as_data(original_obj)

        obj = from_data(TestDataclass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = TestDataclassTuple(123)

        data = as_data(original_obj)

        obj = from_data(TestDataclassTuple, data)

        self.assertEqual(original_obj, obj)

        # Test 3
        original_obj = TestDataclassWithStrictTuple((1, '2', TestDataclass(3)))

        data = as_data(original_obj)

        obj = from_data(TestDataclassWithStrictTuple, data)

        self.assertEqual(original_obj, obj)

    def test_recursive_dataclass_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = RecursiveTestDataclass(123)

        data = as_data(original_obj)

        obj = from_data(RecursiveTestDataclass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = RecursiveTestDataclassTuple(123)

        data = as_data(original_obj)

        obj = from_data(RecursiveTestDataclassTuple, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_optional_parameters_match_after_as_data_from_data(self):
        # Test 1
        original_obj = TestDataclassWithOptionalParameters(159, 21)

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithOptionalParameters, data)

        self.assertEqual(original_obj, obj)

        # Test2
        original_obj = TestDataclassWithOptionalParameters(159, None, "red")

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithOptionalParameters, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_union_parameter_match_after_as_data_from_data(self):
        # Test 1
        original_obj = TestDataclassWithUnionParameter(789, 13)

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithUnionParameter, data)

        self.assertEqual(original_obj, obj)

        # Test2
        original_obj = TestDataclassWithUnionParameter(789, (3, 3))

        data = as_data(original_obj)

        obj  = from_data(TestDataclassWithUnionParameter, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_subclass_member_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = ContainerDataclass(SubDataclassB("Sigmath", "Bits", 6))

        data = as_data(original_obj)

        obj = from_data(ContainerDataclass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = ContainerDataclass(SubDataclassAsTuple("Rainbow", "Dash"))

        data = as_data(original_obj)

        obj = from_data(ContainerDataclass, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_subclass_member_with_default_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = ContainerClassWithDefault(SubDataclassAWithDefault())

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithDefault, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = ContainerClassWithDefault(SubDataclassBWithDefault())

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithDefault, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_union_with_subclass_member_matches_after_as_data_from_data(self):
        # Test 1
        original_obj = ContainerClassWithUnionWithBaseClass(SubDataclassA("Sigmath", "Bits"))

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithUnionWithBaseClass, data)

        self.assertEqual(original_obj, obj)

        # Test 2
        original_obj = ContainerClassWithUnionWithBaseClass(SubDataclassAsTuple("Sigmath", "Bits"))

        data = as_data(original_obj)

        obj = from_data(ContainerClassWithUnionWithBaseClass, data)

        self.assertEqual(original_obj, obj)

    def test_dataclass_with_converters_and_complex_dict_key_types_matches_after_as_data_from_data(self):
        original_obj = DataclassWithComplexTypesAsDictKeys(
            {
                (HashableClass(6), FrozenDataclass((1, 2)), (7, HashableClass(7))): TestIntEnum.ONE,
                (HashableClass(10), FrozenDataclass(()), (1, TestEnum.A)): TestIntEnum.ZERO,
            },
            {
                None: {TestEnum.A, TestIntEnum.TWO, HashableClass(3)},
                FrozenDataclassWithFrozenDataclass((1, 2), FrozenDataclass((3, 4))): {TestIntEnum.TWO, TestEnum.C, TestIntEnum.TWO},
                TestIntEnum.TWO: {HashableClass(2), HashableClass(2)},
            },
            {
                (
                    FrozenDataclassWithFrozenDataclass((0,), FrozenDataclass((0,))),
                    FrozenDataclassWithFrozenDataclass((1,), FrozenDataclass((2, 3))),
                    FrozenDataclassWithFrozenDataclass((2,), FrozenDataclass((3, 4, 5))),
                ): b'Wow!',
                (FrozenDataclassWithFrozenDataclass((3,), FrozenDataclass((3,))),): None,
                (FrozenDataclassWithFrozenDataclass((4,), FrozenDataclass((4,))),): frozenset({"a", "b", "b"}),
                (FrozenDataclassWithFrozenDataclass((5,), FrozenDataclass((5,))),): b'pony',
                (FrozenDataclassWithFrozenDataclass((6,), FrozenDataclass((6,))),): NonDataclass(666),
            },
        )

        def hashable_class_to_str(_obj: HashableClass) -> str:
            return str(_obj.number)
        def str_to_hashable_class(number: str) -> HashableClass:
            return HashableClass(int(number))

        def int_subtypes_to_int(_obj, *, _cls) -> int:
            return int(_obj)
        # int to TestIntEnum done by default constructor

        def bytes_to_str(_obj: bytes) -> str:
            return str(_obj, 'utf-8')
        def str_to_bytes(string: str) -> bytes:
            return bytes(string, 'utf-8')

        def non_dataclass_to_int(_obj: NonDataclass) -> int:
            return _obj.value
        def int_to_non_dataclass(number: int) -> NonDataclass:
            return NonDataclass(number)

        data = as_data(
            original_obj,
            converters={
                HashableClass: hashable_class_to_str,
                int: int_subtypes_to_int,
                bytes: bytes_to_str,
                NonDataclass: non_dataclass_to_int,
            }
        )

        self.assertDictEqual(data, {
            'complex_dict_a': {
                ("6", ((1, 2),), (7, "7")): 1,
                ("10", ((),), (1, TestEnum.A)): 0,
            },
            'complex_dict_b': {
                None: {TestEnum.A, 2, "3"},
                ((1, 2), ((3, 4),)): {2, TestEnum.C},
                2: {"2"},
            },
            'complex_dict_c': {
                (
                    ((0,), ((0,),)),
                    ((1,), ((2, 3),)),
                    ((2,), ((3, 4, 5),)),
                ): "Wow!",
                (((3,), ((3,),)),): None,
                (((4,), ((4,),)),): frozenset({"a", "b", "b"}),
                (((5,), ((5,),)),): "pony",
                (((6,), ((6,),)),): 666,
            },
        })

        obj = from_data(
            DataclassWithComplexTypesAsDictKeys,
            data,
            converters={
                HashableClass: str_to_hashable_class,
                NonDataclass: int_to_non_dataclass,
                bytes: str_to_bytes,
            }
        )

        self.assertEqual(original_obj, obj)


if __name__ == '__main__':
    unittest.main()
