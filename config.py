from typing import Any, Optional, Type, Union

from .field import Field
from . import settings


class ConfigMeta(type):
    def __new__(mcs, name: str, base_class: tuple[Type], attributes: dict[str, Any]) -> Type:
        attributes = mcs._unpack_attributes(mcs, name, base_class, attributes)

        return super().__new__(mcs, name, base_class, attributes)

    def _unpack_attributes(cls, name: str, base_class: tuple[Type], attributes: dict[str, Any]) -> dict[str, Any]:
        unpack_attributes = {}

        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, Field):
                unpack_attributes[attr_name] = attr_value.value
            elif type(attr_value) is type:
                unpack_attributes[attr_name] = ConfigMeta.__new__(cls, attr_name, base_class, attr_value.__dict__)
            else:
                if attr_name == '_prefix_':
                    attr_value = attr_value if attr_name is not None else name.upper()
                unpack_attributes[attr_name] = attr_value

        return unpack_attributes


class Config(metaclass=ConfigMeta):
    _prefix_: Optional[str] = None

    @classmethod
    def as_dict(cls):
        return dict_view(cls)


def is_magic(name: str) -> bool:
    return name.startswith('__') and name.endswith('__')


def dict_view(config: Union[Config, type]) -> dict:
    """
    Returns a dict view for config
    :param config:
    :return:
    """
    return {
        name:
            dict_view(attribute)
            if hasattr(attribute := getattr(config, name), '_prefix_')
            else attribute
        for name in
        filter(lambda name:
               not is_magic(name)
               and (hasattr(getattr(config, name), '_prefix_') or not callable(getattr(config, name))),
               dir(config))
    }


def create_config(settings_parameters: dict, *, config_name: Optional[str] = None) -> Union[Config, type]:
    config_attributes = {}
    for name, value in settings_parameters.items():
        if isinstance(value, dict):
            config_attributes[name] = create_config(value, config_name=name)
        else:
            config_attributes[name] = value

    return type(config_name or settings.DEFAULT_CONFIG_NAME, (Config,), config_attributes)
