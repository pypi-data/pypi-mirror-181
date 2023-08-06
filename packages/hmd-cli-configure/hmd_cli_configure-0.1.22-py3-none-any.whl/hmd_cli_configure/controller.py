import os
from pathlib import Path

import yaml
from cement import Controller, ex
from importlib.metadata import version
from hmd_cli_tools import get_version
from dotenv import set_key

VERSION_BANNER = """
hmd configure version: {}
"""


class LocalController(Controller):
    class Meta:
        label = "configure"
        alias = "config"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Sets environment variables in HMD_HOME"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the configure command.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_configure")),
                },
            ),
        )

    @ex(
        help="Set environment variable in $HMD_HOME/.config/hmd.env",
        arguments=[
            (["key"], {"action": "store"}),
            (["value"], {"action": "store"}),
        ],
    )
    def set_env(self):
        key = self.app.pargs.key
        value = self.app.pargs.value

        hmd_home = os.environ.get("HMD_HOME")

        if hmd_home is None:
            raise Exception("HMD_HOME environment variable is not set.")

        cfg_path = Path(hmd_home) / ".config"

        if not os.path.exists(cfg_path):
            os.mkdir(cfg_path)

        env_path = cfg_path / "hmd.env"

        if not os.path.exists(env_path):
            with open(env_path, "w"):
                pass

        set_key(env_path, key, value)
