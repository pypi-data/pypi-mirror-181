import logging
from copy import deepcopy

from poetry.core.pyproject.toml import PyProjectTOML

PLUGIN_NAME = 'poetry-git-version-plugin'


class PluginConfig(object):
    """Обертка над конфигурацией pyproject"""

    pyproject: PyProjectTOML

    _default_setting = {
        # Игнорирование отсутствия тега
        'ignore_exception': True,
        # Использование ref без тега
        'use_last_tag': True,
    }

    def __init__(self, pyproject: PyProjectTOML) -> None:
        self.pyproject = pyproject

    @property
    def settings(self):
        settings = self.pyproject.data.get('tool', {}).get(PLUGIN_NAME, {})
        return self._default_setting | settings

    @property
    def ignore_exception(self) -> bool:
        return self.settings['ignore_exception']

    @property
    def use_last_tag(self) -> bool:
        return self.settings['use_last_tag']
