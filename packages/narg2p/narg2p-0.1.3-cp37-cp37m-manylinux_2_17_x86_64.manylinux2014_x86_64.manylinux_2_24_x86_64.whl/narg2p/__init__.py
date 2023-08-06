# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""isort:skip_file"""

import os
import sys

try:
    from .version import __version__  # noqa
except ImportError:
    version_txt = os.path.join(os.path.dirname(__file__), "version.txt")
    with open(version_txt) as f:
        __version__ = f.read().strip()

__all__ = ["pdb"]

# backwards compatibility to support `from narg2p.X import Y`
from narg2p.distributed import utils as distributed_utils
from narg2p.logging import meters, metrics, progress_bar  # noqa

sys.modules["narg2p.distributed_utils"] = distributed_utils
sys.modules["narg2p.meters"] = meters
sys.modules["narg2p.metrics"] = metrics
sys.modules["narg2p.progress_bar"] = progress_bar

# initialize hydra
from narg2p.dataclass.initialize import hydra_init
hydra_init()

import narg2p.criterions  # noqa
import narg2p.distributed  # noqa
import narg2p.models  # noqa
import narg2p.modules  # noqa
import narg2p.optim  # noqa
import narg2p.optim.lr_scheduler  # noqa
import narg2p.pdb  # noqa
import narg2p.scoring  # noqa
import narg2p.tasks  # noqa
import narg2p.token_generation_constraints  # noqa
import narg2p.dataclass
import narg2p.data

import narg2p.benchmark  # noqa
import narg2p.model_parallel  # noqa
