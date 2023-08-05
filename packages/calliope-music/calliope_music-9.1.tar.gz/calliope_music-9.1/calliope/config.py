# Calliope
# Copyright (C) 2017,2022  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import *
import configparser
import logging
import os
import pathlib

log = logging.getLogger(__name__)


def _xdg_config_dirs():
    # Code taken from pyxdg module.
    #
    # We avoid using xdg.BaseDirectory here because it reads the environment
    # only on startup and then stores the directories as globals. We want to
    # honour changes in the environment after the start of the process so
    # that click.testing.CliRunner can manage them.
    _home = os.path.expanduser('~')
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.join(_home, '.config')
    return [xdg_config_home] + \
        (os.environ.get('XDG_CONFIG_DIRS') or '/etc/xdg').split(':')


class Configuration:
    """Helper to read configuration values from well-known config file.

    The config file location is determined by the ``XDG_CONFIG_HOME``
    environment variable, usually resolving to
    ``$HOME/.local/calliope/calliope.conf``.

    """
    def __init__(self):
        self.parser = configparser.ConfigParser()
        for config_dir in _xdg_config_dirs():
            config_file = pathlib.Path(config_dir).joinpath('calliope/calliope.conf')
            if config_file.exists():
                log.debug("Reading config from %s", config_file)
                self.parser.read(config_file)

    def get(self, section: str, name: str) -> any:
        """Read a single config value.

        Config key names should be lowercase and use underscore (``_``) to
        separate words. For backwards compatibility reasons, if a key
        ``foo_bar`` is not found in the config, ``foo-bar`` will also be
        checked.

        """
        try:
            return self.parser.get(section, name)
        except (configparser.NoSectionError, configparser.NoOptionError):
            try:
                # For legacy reasons, config files can use key names like
                # `client-id` instead of `client_id`.
                return self.parser.get(section, name.replace('_', '-'))
            except (configparser.NoSectionError, configparser.NoOptionError):
                return None

    def get_section(self, section: str) -> Dict[str, any]:
        """Return all key/value pairs defined in ``section``.

        Any hyphens (``-``) in key names will be converted to underscores
        (``_``).

        """
        try:
            items = [
                (key.replace('-', '_'), value)
                for key, value in self.parser.items(section)
            ]
            return dict(items)
        except configparser.NoSectionError:
            return dict()
