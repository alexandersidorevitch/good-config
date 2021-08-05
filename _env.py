from .casters import BoolCaster, FloatCaster, IntCaster, ListCaster, LoguruLogLevelCaster
from .exceptions import ImpossibleToCastError
from .providers import EnvironmentProvider, AbstractProvider, JsonProvider

_casters = (BoolCaster(), IntCaster(), FloatCaster(), ListCaster(), LoguruLogLevelCaster())

_provider = EnvironmentProvider()


class _ENV:

    def __getattribute__(self, item: str):
        value_from_provider = _provider.get(item.upper())
        for caster in _casters:
            try:
                return caster.cast(value_from_provider)
            except ImpossibleToCastError:
                pass
        return value_from_provider


ENV = _ENV()
# JSON_ENV = _ENV(provider=JsonProvider())
