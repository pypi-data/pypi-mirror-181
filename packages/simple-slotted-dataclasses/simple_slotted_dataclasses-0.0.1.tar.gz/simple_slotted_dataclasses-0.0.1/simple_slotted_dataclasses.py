import dataclasses
import functools
import typing


_Cls = typing.TypeVar("_Cls", bound=object)


__version__ = '0.0.1'



@functools.wraps(dataclasses.dataclass)
def _create_dataclass(
    cls: typing.Optional[_Cls] = None,
    **kwargs,
) -> _Cls:
    return dataclasses.dataclass(cls, **kwargs)  # noqa


@functools.wraps(dataclasses.dataclass)
def dataclass(
    cls: typing.Optional[_Cls] = None,
    slots: bool = True,
    **kwargs,
) -> _Cls:
    def builder(
        cls_: typing.Optional[_Cls] = None,
    ) -> _Cls:
        is_dataclass = dataclasses.is_dataclass(cls_)

        if not slots:
            if is_dataclass:
                return cls_
            return _create_dataclass(cls, **kwargs)

        if not is_dataclass:
            cls_ = _create_dataclass(cls_, **kwargs)

        dc_field_keys = tuple((f.name for f in dataclasses.fields(cls_)))
        dc_dict = {
            k: v for k, v in cls_.__dict__.items()
            if (k != "__dict__") and (k not in dc_field_keys)
        }
        dc_dict["__slots__"] = dc_field_keys

        new_dc = type(cls_.__name__, cls_.__bases__, dc_dict)

        return new_dc

    if cls is None:
        return builder

    return builder(cls)
