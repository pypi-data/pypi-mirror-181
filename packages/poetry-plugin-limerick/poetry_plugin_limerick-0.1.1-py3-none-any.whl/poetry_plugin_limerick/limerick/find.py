"""Functions for finding Cookiecutter templates and other components."""
import logging
import os
from pathlib import Path

from .exceptions import NonTemplatedInputDirException

logger = logging.getLogger(__name__)


def find_template(repo_dir:Path) -> Path:
    """Determine which child directory of ``repo_dir`` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :return: Relative path to project template.
    """
    logger.debug(f'Searching {repo_dir} for the project template.')

    for str_path in repo_dir.glob("**/*"):
        logger.debug(f"str_path: {str_path}")
        if 'cookiecutter' in str_path.__str__() and '{{' in str_path.__str__() and '}}' in str_path.__str__():
            project_template = repo_dir.joinpath(str_path)
            break
    else:
        raise NonTemplatedInputDirException

    logger.debug(f"The project template appears to be {project_template}")
    return project_template