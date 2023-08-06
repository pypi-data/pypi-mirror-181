"""
Main entry point for the `limerick` command.
The code in this module is also a good example of how to use Cookiecutter as a
library rather than a script.
"""
from copy import copy
import logging
import os
import sys
from pathlib import Path
from poetry.poetry import Poetry
from cleo.io.io import IO

from .exceptions import *
from .config import get_user_config
from .repository import determine_repo_dir
from .replay import dump, load
from .generate import generate_context, generate_files
from .prompt import prompt_for_config
from .utils import rmtree

logger = logging.getLogger(__name__)

class Limerick:

    def __init__(self, poetry:Poetry, io:IO, **kwargs):
        self._poetry = poetry
        self.toml_config = self._poetry.local_config
        self._io = io
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
        logger.debug(f"Limerick object: {self.__dict__}")


    def compose(self):
        if self.replay and ((self.no_input is not False) or (self.extra_context is not None)):
            err_msg = (
                "You can not use both replay and no_input or extra_context "
                "at the same time."
            )
            raise InvalidModeException(err_msg)

        config_dict = get_user_config(
            config_file=self.config_file,
            default_config=self.default_config,
        )
        logger.debug(f"config dict: {config_dict}")
        repo_dir, cleanup = determine_repo_dir(
            template=self.template,
            abbreviations=config_dict['abbreviations'],
            clone_to_dir=Path(config_dict['limerick_dir']),
            checkout=self.checkout,
            no_input=self.no_input,
            password=self.password,
            directory=self.relative_dir,
        )

        import_patch = _patch_import_path_for_repo(repo_dir)

        template_name = os.path.basename(os.path.abspath(repo_dir))
        logger.debug(f"Limerick object: {self.__dict__}")
        if self.replay:
            with import_patch:
                if isinstance(self.replay, bool):
                    context = load(Path(config_dict['replay_dir']), template_name)
                else:
                    path, template_name = os.path.split(os.path.splitext(self.replay)[0])
                    context = load(path, template_name)
        else:
            context_file = repo_dir.joinpath('cookiecutter.json')
            logger.debug(f'context_file is {context_file}')
            context = generate_context(
                context_file=context_file,
                default_context=config_dict['default_context'],
                extra_context=self.extra_context,
            )
            with import_patch:
                context['cookiecutter'] = prompt_for_config(context, self.no_input, self.toml_config, self.override_toml)

            # include template dir or url in the context dict
            context['cookiecutter']['_template'] = self.template

            # include output+dir in the context dict
            context['cookiecutter']['_output_dir'] = Path(self.output_dir).absolute().__str__()
            logger.debug(f"replay_dir: {config_dict['replay_dir']}")
            dump(config_dict['replay_dir'], template_name, context)

         # Create project from local context and project template.
        with import_patch:
            result = generate_files(
                repo_dir=repo_dir,
                context=context,
                overwrite_if_exists=self.overwrite_if_exists,
                skip_if_file_exists=self.skip_if_file_exists,
                output_dir=self.output_dir,
                accept_hooks=self.accept_hooks,
                keep_project_on_failure=self.keep_project_on_failure,
            )

        # Cleanup (if required)
        if cleanup:
            rmtree(repo_dir)

        return result




class _patch_import_path_for_repo:
    def __init__(self, repo_dir):
        self._repo_dir = repo_dir
        self._path = None

    def __enter__(self):
        self._path = copy(sys.path)
        sys.path.append(self._repo_dir)

    def __exit__(self, type, value, traceback):
        sys.path = self._path