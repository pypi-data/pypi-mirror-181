from logging import getLogger
from pathlib import Path

import toml
from pkg_resources import DistributionNotFound, get_distribution

log = getLogger(__name__)

# Root path to the Skaha Project
BASE_PATH: Path = Path(__file__).absolute().parent.parent

try:
    __version__ = get_distribution("skaha").version
except DistributionNotFound as error:  # pragma: no cover
    log.warning(error)
    pyproject = toml.load(BASE_PATH / "pyproject.toml")
    __version__ = pyproject["tool"]["poetry"]["version"]
except Exception as error:  # pragma: no cover
    log.warning(error)
    log.warning("unable to find skaha client version")
    __version__ = "unknown"
