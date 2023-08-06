"""Generate random instances of the given Pydantic model type."""
import datetime
import math
import random
import string
import types
import typing
from enum import Enum
from typing import Any, Type, TypeVar
from uuid import UUID, uuid4

import pydantic
from pydantic import BaseModel
from pydantic.fields import ModelField

ModelType = TypeVar("ModelType", bound=BaseModel)


def generate(
    model_type: Type[ModelType],
    use_default_values: bool = True,
    optionals_use_none: bool = False,
    **kwargs: Any,
) -> ModelType:
    """Generate an instance of a Pydantic model with random values.

    Any values provided in `kwargs` will be used as model field values
    instead of randomly generating them.

    :param model_type: Model type to generate an instance of.
    :param use_default_values: Whether to use model default values.
    :param optionals_use_none: How to handle optional fields.
    :param kwargs: Attributes to set on the model instance.
    :return: A randomly generated instance of the provided model type.
    """
    for field_name, model_field in model_type.__fields__.items():
        if field_name in kwargs:
            continue
        if model_field.default is not None or model_field.default_factory is not None:
            if use_default_values:
                continue

        kwargs[field_name] = _get_value(
            model_field.annotation, model_field, use_default_values, optionals_use_none
        )
    return model_type(**kwargs)


def _get_value(
    type_: Type,
    model_field: ModelField,
    use_default_values: bool,
    optionals_use_none: bool,
) -> Any:
    origin = typing.get_origin(type_)
    if origin is dict:
        k_type, v_type = typing.get_args(type_)
        return {
            _get_value(
                k_type, model_field, use_default_values, optionals_use_none
            ): _get_value(v_type, model_field, use_default_values, optionals_use_none)
            for _ in range(random.randint(1, 100))
        }
    if origin is list:
        return [
            _get_value(arg, model_field, use_default_values, optionals_use_none)
            for _ in range(random.randint(1, 100))
            for arg in typing.get_args(type_)
        ]
    if origin and issubclass(origin, types.UnionType):
        type_choices = [
            it for it in typing.get_args(type_) if not issubclass(it, types.NoneType)
        ]
        chosen_union_type = random.choice(type_choices)
        return _get_value(
            chosen_union_type, model_field, use_default_values, optionals_use_none
        )
    if model_field.allow_none and optionals_use_none:
        return None
    if type_ == str or issubclass(type_, pydantic.types.ConstrainedStr):
        return _random_str_value(model_field)
    if type_ == int or isinstance(type_, pydantic.types.ConstrainedNumberMeta):
        return _random_int_value(model_field)
    if type_ == float:
        return random.random() * 100
    if type_ == bool:
        return random.random() > 0.5
    if issubclass(type_, types.NoneType):
        return None
    if issubclass(type_, BaseModel):
        return generate(type_, use_default_values, optionals_use_none)
    if issubclass(type_, Enum):
        return random.choice(list(type_))
    if type_ == UUID:
        return uuid4()
    if type_ == datetime.date:
        return _random_date_value()
    if type_ == datetime.time:
        return _random_time_value()
    if type_ == datetime.timedelta:
        return _random_timedelta_value()
    if type_ == datetime.datetime:
        return _random_datetime_value()
    return type_()


def _random_str_value(model_field: ModelField) -> str:
    """Get a random string."""
    random.choices(string.ascii_letters + string.digits)
    min_len = model_field.field_info.min_length or random.randint(1, 100)
    max_len = model_field.field_info.max_length or random.randint(1, 100) + min_len
    target_length = random.choice(range(min_len, max_len))
    choices = string.ascii_letters + string.digits
    return _random_str(choices, target_length)


def _random_int_value(model_field: ModelField) -> int:
    """Get a random integer."""
    default_max_difference = 256
    iter_size = model_field.field_info.multiple_of or 1
    # Determine lower bound.
    lower = 0
    if ge := model_field.field_info.ge:
        while lower < ge:
            lower += iter_size
    if gt := model_field.field_info.gt:
        while lower <= gt:
            lower += iter_size
    # Determine upper bound.
    upper = lower + iter_size * default_max_difference
    if le := model_field.field_info.le:
        while upper > le:
            upper -= iter_size
    if lt := model_field.field_info.lt:
        while upper >= lt:
            upper -= iter_size
    # Re-evaluate lower bound in case ge/gt unset and upper is negative.
    if not model_field.field_info.ge and not model_field.field_info.gt:
        if lower > upper:
            lower = upper - iter_size * default_max_difference
    # Find a random int within determined range.
    if not model_field.field_info.multiple_of:
        return random.randint(lower, upper)
    max_iter_distance = abs(math.floor((upper - lower) / iter_size))
    return lower + iter_size * random.randint(1, max_iter_distance)


def _random_datetime_value() -> datetime.datetime:
    dt = datetime.datetime.fromordinal(_random_date_value().toordinal())
    dt += _random_timedelta_value()
    return dt


def _random_date_value() -> datetime.date:
    return datetime.date(
        year=random.randint(1970, 2037),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
    )


def _random_time_value() -> datetime.time:
    return datetime.time(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )


def _random_timedelta_value() -> datetime.timedelta:
    return datetime.timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


def _random_str(choices: str, target_length: int) -> str:
    return "".join(random.choice(choices) for _ in range(target_length))
