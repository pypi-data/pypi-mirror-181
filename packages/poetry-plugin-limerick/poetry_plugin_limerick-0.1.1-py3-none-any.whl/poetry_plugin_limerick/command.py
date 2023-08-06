from __future__ import annotations

from cleo.helpers import option, argument
# from packaging.utils import canonicalize_name
from poetry.console.commands.group_command import GroupCommand
from poetry.core.packages.dependency_group import MAIN_GROUP

from .limerick.main import Limerick

class LimerickCommand(GroupCommand):
    name = "limerick"
    description = "Creates boilerplate files using cookiecutter."
    options = [
        option(
            "checkout",
            "c",
            "The branch, tag or commit ID to checkout after clone.",
            flag=False,
            # default=Exporter.FORMAT_REQUIREMENTS_TXT,
        ),
        *GroupCommand._group_dependency_options(),
        option(
            "no-input",
            "i",
            "Prompt the user at command line for manual configuration?",
            flag=True,
        ),
        option(
            "extra-context",
            "e",
            "A dictionary of context that overrides default and user configuration.",
            flag=False,
        ),
        option(
            "replay",
            "r",
            " Do not prompt for input, instead read from saved json. If \
            ``True`` read from the ``replay_dir``. \
            if it exists",
            flag=True,
        ),
        option(
            "overwrite-if-exists",
            "o",
            "Overwrite the contents of the output directory if it exists.",
            flag=True,
        ),
        option(
            "config-file",
            "x",
            "User configuration file path.",
            flag=False,
        ),
        option(
            "default-config",
            "d",
            "Use default values rather than a config file.",
            flag=True,
        ),
        option(
            "password",
            "p",
            "The password to use when extracting the repository.",
            flag=False,
        ),
        option(
            "relative-dir",
            "b",
            "Relative path to a cookiecutter template in a repository.",
            flag=False,            
        ),
        option(
            "skip-if-file-exists",
            "s",
            "Skip the files in the corresponding directories if they already exist",
            flag=True,
        ),
        option(
            "deny-hooks", 
            None,
            "Don't run pre and post hooks if set to `True`.",
            flag=True,
        ),
        option(
            "override-toml",
            "t",
            "Use user input instead of pyproject.toml",
            flag=True,
        ),
        option(
            "keep-project-on-failure",
            "k", 
            "If `True` keep generated project directory even when generation fails",
            flag=True,
        ),
        ]

    arguments = [argument(name="template"), argument(name="output_dir", optional=True, default=".")]

    @property
    def non_optional_groups(self) -> set[str]:
        # method only required for poetry <= 1.2.0-beta.2.dev0
        return {MAIN_GROUP}

    @property
    def default_groups(self) -> set[str]:
        return {MAIN_GROUP}

    def handle(self) -> None:
        print(f"Hello from LimerickCommand v{self.poetry.local_config['version']}")
        args = {arg.name:self.argument(arg.name) for arg in self.arguments}
        opts = {opt.name.replace("-", "_"):self.option(opt.name) for opt in self.options}
        opts['accept_hooks'] = not opts.pop('deny_hooks')
        opts = args | opts
        print(opts)
        limerick = Limerick(self.poetry, self.io, **opts)
        limerick.compose()