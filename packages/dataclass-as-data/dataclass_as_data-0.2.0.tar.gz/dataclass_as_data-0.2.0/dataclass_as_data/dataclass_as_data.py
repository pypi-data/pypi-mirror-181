from __future__ import annotations

import functools
import inspect
from abc import ABC
from contextlib import suppress
from dataclasses import is_dataclass, fields

from typing import TypeVar, Optional, Union, Type, Callable, Any, get_origin, get_args, get_type_hints, Iterable

__all__ = (
    'as_data', 'as_dict', 'as_tuple',
    'from_data', 'from_dict', 'from_tuple',

    # Classes
    'default_converter',
    'DataAsTuple',
)


_NONE_TYPE = type(None)
_PRIMITIVE_VALUES = {str, int, bool, float, bytes, bytearray, _NONE_TYPE}
_PRIMITIVE_CONTAINERS = {list, set, frozenset}
_PRIMITIVES = _PRIMITIVE_VALUES | _PRIMITIVE_CONTAINERS | {dict, tuple}


Data = Union[dict, tuple, list]
ConverterFunction = Callable[[Any], Any]
ConverterFunctionsDict = dict[type, ConverterFunction]
ConvertersDict = dict[type, '_Converter']

T = TypeVar('T')
TType = TypeVar('TType', bound=type)


class default_converter:
    """A type used to signify the default converter to use when converting types using the `converters` parameter."""


class DataAsTuple(ABC):
    def as_data(self, *, converters):
        return as_tuple(self, converters=converters)

    @classmethod
    def from_data(cls, data, *, converters):
        return from_tuple(cls, data, converters=converters)


class _Converter:
    def __init__(self, converter: ConverterFunction):
        self.converter = converter

        if not isinstance(converter, type):
            parameters = inspect.signature(converter).parameters
            last_parameter = parameters[next(reversed(parameters))]

            self._cls_kwarg = last_parameter if last_parameter.kind == inspect.Parameter.KEYWORD_ONLY else None
        else:
            self._cls_kwarg = None

    @functools.cached_property
    def has_cls_kwarg(self) -> bool:
        return self._cls_kwarg is not None

    def __call__(self, obj: Any, *, cls: Optional[type] = None) -> Any:
        if self._cls_kwarg is not None:
            return self.converter(obj, **{self._cls_kwarg.name: cls})  # type: ignore
        else:
            return self.converter(obj)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.converter})"


def _deep(func: Callable[..., T]):
    """Makes a single-input function apply deeply to all values in a nested data structure of dicts, tuples, and lists"""
    @functools.wraps(func)
    def wrapper(data: Any, *args, **kwargs) -> Union[dict, tuple, list, set, frozenset, T]:
        if isinstance(data, dict):
            return {_as_data(key, *args, **{**kwargs, 'as_tuple_default': True}): wrapper(val, *args, **kwargs) for key, val in data.items()}
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(wrapper(val, *args, **kwargs) for val in data)
        return func(data, *args, **kwargs)
    return wrapper


## as_data
def as_data(obj: Any, /, *, converters: Optional[ConverterFunctionsDict] = None) -> Data:
    """
    Transforms the dataclass into a sequential data object (dict or tuple).
    Applies recursively to all parameters that are also dataclasses.

    This behaviour can be overridden by defining an `as_data` method in your dataclass.
    This only supports other dataclasses, primitive types, and primitive containers (dict, list, tuple).

    Optionally specify `converters` to specify how non-dataclasses should be converted.
    To override this default, specify a converter function for the `dataclass_as_data.default_converter` type.

    @param obj: The dataclass object instance
    @param converters: An optional dictionary of types to single-input functions
    @return: The dataclass represented as a dict or tuple
    """
    return _as_data(obj, converters=_create_converters(converters) if converters is not None else None)


@_deep
def _as_data(
        obj: Any, /, *,
        converters: Optional[ConvertersDict] = None,
        annotate: bool = False,
        as_tuple_default: bool = False
) -> Data:
    """
    @param obj: The dataclass object instance
    @param converters: An optional dictionary of types to single-input functions
    @param annotate: Whether to annotate the dataclass type explicitly in the generated data.
    If True, `from_data` will use this when converting back as long as it is a compatible type.
    @param as_tuple_default: Whether to use as_tuple as the default instead of as_dict
    @return: The dataclass represented as a dict or tuple
    """
    data = _call_with_optional_kwargs(obj.as_data, converters=_unpack_converters(converters)) \
        if hasattr(obj, 'as_data') else None

    if is_dataclass(obj):
        data = data if data is not None else _as_tuple(obj, converters=converters, as_tuple_default=True) \
            if as_tuple_default else _as_dict(obj, converters=converters)
    else:
        return data if data is not None else _convert(obj, converters=converters)

    if annotate:
        if isinstance(data, dict):
            data['__type'] = type(obj).__name__
        elif isinstance(data, (tuple, list)):
            data = (*data, '__type', type(obj).__name__)

    return data


def as_dict(data_class_obj: Any, /, *, converters: Optional[ConverterFunctionsDict] = None) -> dict:
    """
    Return a dataclass object as a dictionary representation.
    @param data_class_obj: The dataclass object
    @param converters: An optional dictionary of types to single-input functions
    @return: The dataclass represented as a dict
    """
    if isinstance(data_class_obj, type) or not is_dataclass(data_class_obj):
        raise TypeError(f"`data_class_obj` must be an instance of a dataclass")

    return _as_dict(data_class_obj, converters=_create_converters(converters) if converters is not None else None)


def _as_dict(data_class_obj: Any, /, *, converters: Optional[ConvertersDict] = None) -> dict:
    """
    @param data_class_obj: The dataclass object
    @param converters: An optional dictionary of types to single-input functions
    @return: The dataclass represented as a dict
    """
    type_hints = get_type_hints(type(data_class_obj))

    return {
        _field.name: _as_data(
            obj := getattr(data_class_obj, _field.name),
            converters=converters,
            annotate=not _exactly_matches_type_hint(type_hints[_field.name], obj),
        ) for _field in fields(data_class_obj) if _field.init
    }


def as_tuple(data_class_obj: Any, /, *, converters: Optional[ConverterFunctionsDict] = None) -> tuple:
    """
    Return a dataclass object as a tuple representation.
    @param data_class_obj: The dataclass object
    @param converters: An optional dictionary of types to single-input functions
    @return: The dataclass represented as a tuple
    """
    if isinstance(data_class_obj, type) or not is_dataclass(data_class_obj):
        raise TypeError(f"`data_class_obj` must be an instance of a dataclass")

    return _as_tuple(data_class_obj, converters=_create_converters(converters) if converters is not None else None)


def _as_tuple(data_class_obj: Any, /, *, converters: Optional[ConvertersDict] = None, as_tuple_default: bool = False) -> tuple:
    """
    @param data_class_obj: The dataclass object
    @param converters: An optional dictionary of types to single-input functions
    @param as_tuple_default: Whether to use as_tuple as the default for all further conversions instead of as_dict
    @return: The dataclass represented as a tuple
    """
    type_hints = get_type_hints(type(data_class_obj))

    return tuple(
        _as_data(
            obj := getattr(data_class_obj, _field.name),
            converters=converters,
            annotate=not _exactly_matches_type_hint(type_hints[_field.name], obj),
            as_tuple_default=as_tuple_default,
        ) for _field in fields(data_class_obj) if _field.init
    )


## from_data
def from_data(data_class: Type[T], /, data: Data, *, converters: Optional[ConverterFunctionsDict] = None) -> T:
    """
    Constructs the given dataclass using the provided data performing conversions with dataclass type hints.
    This behaviour can be overridden by defining a `from_data` class method in your dataclass.

    This only supports other dataclasses, primitive types, and primitive containers (dict, list, tuple).

    Optionally specify `converters` to specify how non-dataclasses should be constructed.
    To override this default, specify a converter function for the `dataclass_as_data.default_converter` type.

    @param data_class: The dataclass to create
    @param data: The data to convert in the form of a dict, tuple, or list
    @param converters: An optional dictionary of types to single-input functions
    @return: The dataclass object instance
    """
    if not isinstance(data_class, type) or not is_dataclass(data_class):
        raise TypeError("`data_class` must be a dataclass type")

    return _from_data(
        data_class, # type: ignore
        data,
        converters=_create_converters(converters) if converters is not None else None,
    )


def _from_data(_type: Type[T], /, data: Data, *, converters: Optional[ConvertersDict] = None) -> T:
    """
    @param _type: The type to create
    @param data: The data to convert in the form of a dict, tuple, or list
    @param converters: An optional dictionary of types to single-input functions
    @return: The type instance constructed from the data
    """
    if is_dataclass(_type):
        matching_types = _matching_types(_type)

        # Handle explicit typing
        type_name = \
            data.get('__type') if isinstance(data, dict) \
            else data[-1] if len(data) >= 2 and data[-2] == '__type' \
            else None

        if type_name is not None:
            if isinstance(data, (tuple, list)):
                data = data[:-2]

            with suppress(StopIteration):
                matching_types = [next(t for t in matching_types if t.__name__ == type_name)]

        exception = None
        for data_class in matching_types:
            try:
                if hasattr(data_class, 'from_data'):
                    return _call_with_optional_kwargs(
                        data_class.from_data,  # type: ignore [attr-defined]
                        data,
                        converters=_unpack_converters(converters)
                    )
                elif isinstance(data, dict):
                    return _from_dict(data_class, data, converters=converters)
                elif isinstance(data, (list, tuple)):
                    return _from_tuple(data_class, tuple(data), converters=converters)
            except (TypeError, ValueError) as e:
                if exception is None:
                    exception = e  # Capture first error

        raise TypeError(f"Cannot convert to dataclass {_type!r} from data {data!r}") from exception


    if (origin := get_origin(_type)) is None or (args := get_args(_type)) is None:
        if not isinstance(_type, type):
            return _type(data)  # Parameter function converter

        # Plain type conversion
        matching_types = _matching_types(_type)
        for matching_type in matching_types:
            with suppress(TypeError, ValueError):
                if hasattr(matching_type, 'from_data'):
                    return matching_type.from_data(data)  # type: ignore [attr-defined]
                else:
                    return _convert(
                        data,
                        converters=converters,
                        obj_type=matching_type,
                    )

        raise TypeError(f"Cannot convert to type {_type!r} or any of its subclasses from data {data!r}")


    if origin in _PRIMITIVE_CONTAINERS:
        return origin(_from_data(args[0], value, converters=converters) for value in data)  # type: ignore [return-value]
    elif origin is tuple:
        if len(args) > 1 and args[1] is Ellipsis:
            return tuple(_from_data(args[0], value, converters=converters) for value in data)  # type: ignore [return-value]

        if len(args) != len(data):
            raise TypeError(f"Incorrect number of elements to convert to type {_type!r} from data {data!r}")

        return tuple(_from_data(arg, value, converters=converters) for arg, value in zip(args, data))  # type: ignore [return-value]
    elif origin is dict and isinstance(data, dict):
        return {  # type: ignore [return-value]
            _from_data(args[0], key, converters=converters): _from_data(args[1], value, converters=converters)
            for key, value in data.items()
        }
    elif origin is Union:
        if _NONE_TYPE in args and data is None:  # typing.Optional
            return None

        args = tuple(_sort_types(args, data=data))

        for arg in args:
            with suppress(TypeError):
                return _from_data(arg, data, converters=converters)

        raise TypeError(f"Data didn't match any of the types in {_type!r}: {data!r}")

    raise TypeError(f"Cannot handle conversions to {_type!r}")


def from_dict(data_class: Type[T], _dict: dict, /, *, converters: Optional[ConverterFunctionsDict] = None) -> T:
    """
    Construct a dataclass object of type `data_class` from a given dictionary
    @param data_class: The dataclass to create
    @param _dict: The dict representation of the dataclass
    @param converters: An optional dictionary of types to single-input functions
    @return: A dataclass instance construction from the dict data
    """
    if not isinstance(data_class, type) or not is_dataclass(data_class):
        raise TypeError("`data_class` must be a dataclass type")

    return _from_dict(
        data_class,  # type: ignore
        _dict,
        converters=_create_converters(converters) if converters is not None else None,
    )


def _from_dict(data_class: Type[T], _dict: dict, /, *, converters: Optional[ConvertersDict] = None) -> T:
    """
    @param data_class: The dataclass to create
    @param _dict: The dict representation of the dataclass
    @param converters: An optional dictionary of types to single-input functions
    @return: A dataclass instance construction from the dict data
    """
    type_hints = get_type_hints(data_class)
    fields_set = {_field.name for _field in fields(data_class)}

    return data_class(**{
        name: _from_data(type_hints[name], value, converters=converters)
        for name, value in _dict.items() if name in fields_set
    })


def from_tuple(data_class: Type[T], _tuple: tuple, /, *, converters: Optional[ConverterFunctionsDict] = None) -> T:
    """
    Construct a dataclass object of type `data_class` from a given tuple.
    @param data_class: The dataclass to create
    @param _tuple: The tuple representation of the dataclass
    @param converters: An optional dictionary of types to single-input functions
    @return: A dataclass instance constructed from the tuple data
    """
    if not isinstance(data_class, type) or not is_dataclass(data_class):
        raise TypeError("`data_class` must be a dataclass type")

    return _from_tuple(
        data_class,  # type: ignore
        _tuple,
        converters=_create_converters(converters) if converters is not None else None,
    )


def _from_tuple(data_class: Type[T], _tuple: tuple, /, *, converters: Optional[ConvertersDict] = None) -> T:
    """
    @param data_class: The dataclass to create
    @param _tuple: The tuple representation of the dataclass
    @param converters: An optional dictionary of types to single-input functions
    @return: A dataclass instance constructed from the tuple data
    """
    type_hints = get_type_hints(data_class)

    return data_class(*(
        _from_data(type_hints[_field.name], value, converters=converters)
        for value, _field in zip(_tuple, fields(data_class))
    ))


def _convert(
        obj_data: T, /, *,
        converters: Optional[ConvertersDict] = None,
        obj_type: Optional[type] = None,
) -> Any:
    """
    Convert the object or data by type as specified in `converters`.
     By default, it is converted to its own type if it doesn't match.
    @param obj_data: The object or data to potentially convert
    @param converters: An optional dictionary of types to single-input functions
    @param obj_type: The object type of the output, if this differs from the input
    """
    converters = converters if converters is not None else {}
    obj_type = obj_type if obj_type is not None else type(obj_data)

    for _type in obj_type.__mro__:
        converter = converters.get(_type)
        if converter is None:
            continue

        if not converter.has_cls_kwarg and _type is not obj_type:
            continue

        return converter(obj_data, cls=obj_type)

    if obj_type in _PRIMITIVES:  # Primitives are not affected by the default converter
        return obj_type(obj_data) if obj_type is not _NONE_TYPE else None

    if default_converter in converters:
        return converters[default_converter](obj_data, cls=obj_type)
    elif type(obj_data) is not obj_type:
        return obj_type(obj_data)

    return obj_data


def _sort_types(types: Iterable[TType], *, data: Any) -> Iterable[TType]:
    """Reorders the types listed in types in categories as follows:
    1. Dataclasses
    2. Type that matches the data type exactly
    3. str is last, as anything will convert to a string

    And removes NoneType.

    @param types: An iterable of types to reorder
    @param data: the data whose type to check for matches against
    @return: An iterable of the types reordered
    """
    data_type = type(data)

    return sorted(
        (t for t in types if t is not _NONE_TYPE),
        key=lambda t: (
            is_dataclass(t),  # 1. Dataclasses
            data_type is t,   # 2. Type that matches the data type exactly
            t is not str,     # 3. str is last
        ),
        reverse=True,
    )


def _create_converters(converter_functions: ConverterFunctionsDict) -> ConvertersDict:
    return {_type: _Converter(function) for _type, function in converter_functions.items()}


def _unpack_converters(converters: Optional[ConvertersDict]) -> Optional[ConverterFunctionsDict]:
    return {_type: converter.converter for _type, converter in converters.items()} if converters is not None else None


def _call_with_optional_kwargs(function: Callable[..., T], *args, **kwargs) -> T:
    try:
        return function(*args, **kwargs)
    except TypeError:
        return function(*args)


def _exactly_matches_type_hint(type_hint: type, obj: Any) -> bool:
    """
    Checks if an instance of an object exactly matches a type hint, disallowing matching any subclasses
    Only works for raw types and list, tuple, dict, and Union generics
    @param type_hint: The type hint
    @param obj: The object instance to check
    @return: Whether the object instance matches the type hint exactly
    """
    if (origin := get_origin(type_hint)) is None or (args := get_args(type_hint)) is None:
        return type(obj) is type_hint

    if origin in _PRIMITIVE_CONTAINERS:
        return type(obj) is origin and all(_exactly_matches_type_hint(args[0], entry) for entry in obj)
    elif origin is tuple:
        if len(args) > 1 and args[1] is Ellipsis:
            return type(obj) is tuple and all(_exactly_matches_type_hint(args[0], entry) for entry in obj)

        return type(obj) is tuple and len(obj) == len(args) \
               and all(_exactly_matches_type_hint(arg, entry) for arg, entry in zip(args, obj))
    elif origin is dict and isinstance(obj, dict):
        return type(obj) is dict \
               and all(_exactly_matches_type_hint(args[0], key) and _exactly_matches_type_hint(args[1], value)
                       for key, value in obj.items())
    elif origin is Union:
        if _NONE_TYPE in args and obj is None:  # typing.Optional
            return True

        for arg in args:
            if _exactly_matches_type_hint(arg, obj):
                return True
        else:
            return False

    return False


def _matching_types(_type: TType, /) -> list[TType]:
    """
    Return all types matching `_type`, starting with `_type`, then all its subclasses, then all their subclasses, etc.
    @param _type: The type
    @return: A list of all the types matching `_type`
    """
    if _type in _PRIMITIVES:  # Primitives are treated purely as-is
        return [_type]

    matching_types = [_type]
    subclasses = _type.__subclasses__()
    while subclasses:
        matching_types.extend(subclasses)
        subclasses = [sub_subclass for subclass in subclasses for sub_subclass in subclass.__subclasses__()]

    return matching_types
