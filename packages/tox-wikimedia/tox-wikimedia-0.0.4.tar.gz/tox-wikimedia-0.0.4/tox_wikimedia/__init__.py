"""
Copyright (C) 2019-2020 Kunal Mehta <legoktm@debian.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from configparser import ConfigParser
import pluggy
import os
from tox.config import Config, DepConfig
from tox.reporter import verbosity2

hookimpl = pluggy.HookimplMarker("tox")


"""
Pre-configured tools

description: Output when `tox -av` is used
commands: Commands to run, can be parameterized by using {} which get formatted
          with the contents of the [wikimedia] section in tox.ini
deps: Packages that need installation
requirements: Install deps from requirements.txt and similarly named variants
"""
TOOLS: dict = {
    "flake8": {
        "description": "Style consistency checker",
        "commands": ["flake8"],
        "deps": ["flake8"],
    },
    "mypy": {
        "description": "Static type checker",
        "commands": ["mypy", "{mypy_package}"],
        "deps": ["mypy"],
        "requirements": True,
    },
    "pytest": {
        "description": "Run tests",
        "commands": ["pytest"],
        "deps": ["pytest"],
        "requirements": True,
    },
}


def get_config(toxinidir: str) -> ConfigParser:
    # TODO: is there a tox API to read this?
    toxini = os.path.join(toxinidir, "tox.ini")
    assert os.path.exists(toxini)
    config = ConfigParser()
    config.read(toxini)
    return config


@hookimpl
def tox_configure(config: Config) -> None:
    # Only run if we're enabled
    toxinidir = str(config.toxinidir)
    cfg = get_config(toxinidir)
    if "wikimedia" not in cfg:
        verbosity2("[wikimedia] tox-wikimedia is not enabled, skipping")
        return

    verbosity2("[wikimedia] tox-wikimedia is enabled")
    for envname, econfig in config.envconfigs.items():
        for factor in econfig.factors:
            # factors are py35, flake8, pytest, etc.
            try:
                fconfig: dict = TOOLS[factor]
            except KeyError:
                continue

            for dep in fconfig["deps"]:
                # Check to make sure the dep is not already
                # specific (e.g. to specify a constraint)
                for cdep in econfig.deps:
                    if dep in cdep.name:
                        break
                else:
                    econfig.deps.append(DepConfig(dep))
                    verbosity2(
                        f"[wikimedia] {envname}: Adding dep on {dep}"
                    )
            if fconfig.get("requirements"):
                for txtdep in [
                    "requirements.txt",
                    "test-requirements.txt",
                ]:
                    if os.path.exists(os.path.join(toxinidir, txtdep)):
                        verbosity2(
                            "[wikimedia] {}: Adding dep on {}".format(
                                envname, txtdep
                            )
                        )
                        econfig.deps.append(DepConfig(f"-r{txtdep}"))
            if econfig.commands:
                verbosity2(
                    "[wikimedia] {}: overridden commands: {}".format(
                        envname, repr(econfig.commands)
                    )
                )
            if not econfig.commands:
                # If there's no command, then set one
                cmd = []
                for part in fconfig["commands"]:
                    if "{" in part:
                        # Needs formatting
                        part = part.format(**cfg["wikimedia"])
                    cmd.append(part)
                econfig.commands.append(cmd)
                verbosity2(
                    "[wikimedia] {}: Setting command to {}".format(
                        envname, str(cmd)
                    )
                )
            if not econfig.description:
                econfig.description = fconfig["description"]
