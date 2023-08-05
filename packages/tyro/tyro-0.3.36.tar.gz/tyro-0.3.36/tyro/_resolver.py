"""Utilities for resolving types and forward references."""
import collections.abc
import copy
import dataclasses
import sys
import types
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    FrozenSet,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import Annotated, get_args, get_origin, get_type_hints

TypeOrCallable = TypeVar("TypeOrCallable", Type, Callable)


def unwrap_origin_strip_extras(typ: TypeOrCallable) -> TypeOrCallable:
    """Returns the origin, ignoring typing.Annotated, of typ if it exists. Otherwise, returns typ."""
    # TODO: Annotated[] handling should be revisited...
    typ, _ = unwrap_annotated(typ)
    origin = get_origin(typ)
    if origin is None:
        return typ
    else:
        return origin


def is_dataclass(cls: Union[Type, Callable]) -> bool:
    """Same as `dataclasses.is_dataclass`, but also handles generic aliases."""
    return dataclasses.is_dataclass(unwrap_origin_strip_extras(cls))


def resolve_generic_types(
    cls: TypeOrCallable,
) -> Tuple[TypeOrCallable, Dict[TypeVar, Type[Any]]]:
    """If the input is a class: no-op. If it's a generic alias: returns the origin
    class, and a mapping from typevars to concrete types."""

    origin_cls = get_origin(cls)

    type_from_typevar = {}
    if (
        # Apply some heuristics for generic types. Should revisit this.
        origin_cls is not None
        and hasattr(origin_cls, "__parameters__")
        and hasattr(origin_cls.__parameters__, "__len__")
    ):
        typevars = origin_cls.__parameters__
        typevar_values = get_args(cls)
        print(typevars, typevar_values, origin_cls)
        assert len(typevars) == len(typevar_values)
        cls = origin_cls
        type_from_typevar.update(dict(zip(typevars, typevar_values)))

    if hasattr(cls, "__orig_bases__"):
        bases = getattr(cls, "__orig_bases__")
        for base in bases:
            origin_base = unwrap_origin_strip_extras(base)
            if origin_base is base or not hasattr(origin_base, "__parameters__"):
                continue
            typevars = origin_base.__parameters__
            typevar_values = get_args(base)
            type_from_typevar.update(dict(zip(typevars, typevar_values)))

    return cls, type_from_typevar


def resolved_fields(cls: Type) -> List[dataclasses.Field]:
    """Similar to dataclasses.fields(), but includes dataclasses.InitVar types and
    resolves forward references."""

    assert dataclasses.is_dataclass(cls)
    fields = []
    annotations = get_type_hints(cls, include_extras=True)
    for field in getattr(cls, "__dataclass_fields__").values():
        # Avoid mutating original field.
        field = copy.copy(field)

        # Resolve forward references.
        field.type = annotations[field.name]

        # Skip ClassVars.
        if get_origin(field.type) is ClassVar:
            continue

        # Unwrap InitVar types.
        if isinstance(field.type, dataclasses.InitVar):
            field.type = field.type.type

        fields.append(field)

    return fields


def is_namedtuple(cls: Type) -> bool:
    return (
        hasattr(cls, "_fields")
        # `_field_types` was removed in Python >=3.9.
        # and hasattr(cls, "_field_types")
        and hasattr(cls, "_field_defaults")
    )


def type_from_typevar_constraints(typ: Union[Type, TypeVar]) -> Union[Type, TypeVar]:
    """Try to concretize a type from a TypeVar's bounds or constraints. Identity if
    unsuccessful."""
    if isinstance(typ, TypeVar):
        if typ.__bound__ is not None:
            # Try to infer type from TypeVar bound.
            return typ.__bound__
        elif len(typ.__constraints__) > 0:
            # Try to infer type from TypeVar constraints.
            return Union.__getitem__(typ.__constraints__)  # type: ignore
    return typ


# Be a little bit permissive with types here, since we often blur the lines between
# Callable[..., T] and Type[T]... this could be cleaned up!
TypeT = TypeVar("TypeT", bound=Callable)


def narrow_type(typ: TypeT, default_instance: Any) -> TypeT:
    """Type narrowing: if we annotate as Animal but specify a default instance of Cat, we
    should parse as Cat.

    This should generally only be applied to fields used as nested structures, not
    individual arguments/fields. (if a field is annotated as Union[int, str], and a
    string default is passed in, we don't want to narrow the type to always be
    strings!)"""
    try:
        potential_subclass = type(default_instance)

        if potential_subclass is type:
            # Don't narrow to `type`. This happens when the default instance is a class;
            # it doesn't really make sense to parse this case.
            return typ

        superclass = unwrap_annotated(typ)[0]

        # For Python 3.10: don't narrow union types.
        if get_origin(superclass) is Union:
            return typ

        if superclass is Any or issubclass(potential_subclass, superclass):  # type: ignore
            if get_origin(typ) is Annotated:
                return Annotated.__class_getitem__(  # type: ignore
                    (potential_subclass,) + get_args(typ)[1:]
                )
            typ = cast(TypeT, potential_subclass)
    except TypeError:
        pass

    return typ


def narrow_container_types(typ: TypeT, default_instance: Any) -> TypeT:
    """Type narrowing for containers. Infers types of container contents."""
    if typ is list and isinstance(default_instance, list):
        typ = List.__getitem__(Union.__getitem__(tuple(map(type, default_instance))))  # type: ignore
    elif typ is set and isinstance(default_instance, set):
        typ = Set.__getitem__(Union.__getitem__(tuple(map(type, default_instance))))  # type: ignore
    elif typ is tuple and isinstance(default_instance, tuple):
        typ = Tuple.__getitem__(tuple(map(type, default_instance)))  # type: ignore
    return typ


MetadataType = TypeVar("MetadataType")


def unwrap_annotated(
    typ: TypeOrCallable, search_type: Optional[Type[MetadataType]] = None
) -> Tuple[TypeOrCallable, Tuple[MetadataType, ...]]:
    """Helper for parsing typing.Annotated types.

    Examples:
    - int, int => (int, ())
    - Annotated[int, 1], int => (int, (1,))
    - Annotated[int, "1"], int => (int, ())
    """
    if not hasattr(typ, "__metadata__"):
        return typ, ()

    args = get_args(typ)
    assert len(args) >= 2

    # Don't search for a specific metadata type if `None` is passed in.
    if search_type is None:
        return args[0], ()

    # Look through metadata for desired metadata type.
    targets = tuple(x for x in args[1:] if isinstance(x, search_type))
    return args[0], targets


def apply_type_from_typevar(
    typ: TypeOrCallable, type_from_typevar: Dict[TypeVar, Type[Any]]
) -> TypeOrCallable:
    if typ in type_from_typevar:
        return type_from_typevar[typ]  # type: ignore

    if len(get_args(typ)) > 0:
        args = get_args(typ)
        if get_origin(typ) is Annotated:
            args = args[:1]
        if get_origin(typ) is collections.abc.Callable:
            assert isinstance(args[0], list)
            args = tuple(args[0]) + args[1:]

        # Convert Python 3.9 and 3.10 types to their typing library equivalents, which
        # support `.copy_with()`.
        if sys.version_info[:2] >= (3, 9):
            shim_table = {
                # PEP 585. Requires Python 3.9.
                tuple: Tuple,
                list: List,
                dict: Dict,
                set: Set,
                frozenset: FrozenSet,
            }
            if hasattr(types, "UnionType"):  # type: ignore
                # PEP 604. Requires Python 3.10.
                shim_table[types.UnionType] = Union  # type: ignore

            for new, old in shim_table.items():
                if isinstance(typ, new) or get_origin(typ) is new:  # type: ignore
                    typ = old.__getitem__(args)  # type: ignore

        return typ.copy_with(tuple(apply_type_from_typevar(x, type_from_typevar) for x in args))  # type: ignore

    return typ
