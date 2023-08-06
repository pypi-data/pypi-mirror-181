# coding=utf8
from dataclasses import dataclass
from typing import overload

from PyQt6.QtCore import QSettings


@dataclass
class SettingInfo:
    key: str
    default: ...


class Settings:
    @staticmethod
    @overload
    def read(*, setting_info: SettingInfo, source='global') -> ...: ...
    @staticmethod
    @overload
    def read(*, key: str, default: ..., source='global') -> ...: ...

    @staticmethod
    def read(*, source='global', **kwargs) -> ...:
        if 'setting_info' in kwargs:
            key = kwargs['setting_info'].key
            default = kwargs['setting_info'].default
        else:
            key = kwargs['key'].key
            default = kwargs['default'].default

        field_path = '/'.join([source, key])
        read_value = QSettings().value(field_path, default)
        if isinstance(read_value, dict) and isinstance(default, dict):
            # Ensure new default fields are present in result value
            value = dict(default)
            value.update(read_value)
            return value
        else:
            return read_value

    @staticmethod
    @overload
    def write(*, setting_info: SettingInfo, value: ..., source='global'): ...
    @staticmethod
    @overload
    def write(*, key: str, value: ..., source='global'): ...

    @staticmethod
    def write(*, value: ..., source='global', **kwargs):
        if 'setting_info' in kwargs:
            key = kwargs['setting_info'].key
        else:
            key = kwargs['key'].key

        field_path = '/'.join([source, key])
        settings = QSettings()
        settings.setValue(field_path, value)
