from __future__ import annotations

from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry

from poetry_git_version_plugin import config
from poetry_git_version_plugin.commands import GitVersionCommand
from poetry_git_version_plugin.exceptions import PluginException, plugin_exception_wrapper
from poetry_git_version_plugin.services import GitVersionService


class PoetryGitVersionPlugin(Plugin):
    """Плагин определения версии по гит тегу"""

    @plugin_exception_wrapper
    def activate(self, poetry: Poetry, io: IO):
        io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Init', Verbosity.VERBOSE)

        self.plugin_config = config.PluginConfig(poetry.pyproject)

        try:
            tag = GitVersionService(io, self.plugin_config).get_tag()

        except Exception as ex:
            if self.plugin_config.ignore_exception:
                if not isinstance(ex, PluginException):
                    ex = PluginException(ex)

                text = f'{ex}. Ignore Exception\n'

                io.write_error(text, Verbosity.VERBOSE)
                return

            raise ex

        if tag is not None:
            poetry.package.version = tag

        io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Finished\n', Verbosity.VERBOSE)


class PoetryGitVersionApplicationPlugin(ApplicationPlugin):
    commands = [GitVersionCommand]
