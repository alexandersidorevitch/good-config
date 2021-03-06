import logging
import typing

from .exceptions import ImpossibleToCastError

VT = typing.TypeVar('VT')


class AbstractCaster:
    def cast(self, val: str) -> typing.Union[typing.Any, typing.NoReturn]:
        """Try to cast or return val"""
        raise NotImplementedError()


class NothingCaster(AbstractCaster):
    """Caster who does nothing"""

    def cast(self, val: str) -> str:
        return val


DEFAULT_CASTER = NothingCaster()


class ConstantCaster(AbstractCaster, typing.Generic[VT]):
    ABLE_TO_CAST: typing.Dict[
        str, typing.Any
    ] = {}

    def cast(self, val: str) -> typing.Union[VT, typing.NoReturn]:
        """Cast using ABLE_TO_CAST dictionary as in BoolCaster"""
        if val.lower() in self.ABLE_TO_CAST:
            converted = self.ABLE_TO_CAST.get(val.lower())
            return typing.cast(VT, converted)

        raise ImpossibleToCastError(val, self)


class BoolCaster(ConstantCaster):
    ABLE_TO_CAST = {
        'TRUE': True,
        '1': True,
        'YES': True,
        'OK': True,
        'ON': True,
        'FALSE': False,
        '0': False,
        'NO': False,
        'OFF': False,
    }


class IntCaster(AbstractCaster):
    def cast(self, val: str) -> typing.Union[int, typing.NoReturn]:
        try:
            return int(val)
        except ValueError:
            raise ImpossibleToCastError(val, self)


class FloatCaster(AbstractCaster):
    def cast(self, val: str) -> typing.Union[float, typing.NoReturn]:
        val = val.replace(',', '.')
        try:
            return float(val)
        except ValueError:
            raise ImpossibleToCastError(val, self)


class ListCaster(AbstractCaster):
    def __init__(self, separator: str = ',', item_caster: AbstractCaster = DEFAULT_CASTER):
        self.separator = separator
        self.item_caster = item_caster

    def cast(self, val: str) -> list:
        if val.endswith(self.separator):
            val = val[0: len(val) - len(self.separator)]

        return list(map(self.item_caster.cast, val.split(self.separator)))


class LoguruLogLevelCaster(ConstantCaster):
    levels = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    ABLE_TO_CAST = {level.lower(): level for level in levels}


__all__ = (
    'BoolCaster',
    'IntCaster',
    'FloatCaster',
    'ListCaster',
    'LoguruLogLevelCaster',
    'AbstractCaster',
    'ConstantCaster',
    'DEFAULT_CASTER',
)
