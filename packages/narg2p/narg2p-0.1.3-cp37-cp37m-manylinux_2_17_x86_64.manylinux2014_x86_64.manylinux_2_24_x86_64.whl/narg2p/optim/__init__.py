# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""isort:skip_file"""

import importlib
import os

from narg2p import registry
from narg2p.optim.bmuf import FairseqBMUF  # noqa
from narg2p.optim.narg2p_optimizer import (  # noqa
    FairseqOptimizer,
    LegacyFairseqOptimizer,
)
from narg2p.optim.fp16_optimizer import FP16Optimizer, MemoryEfficientFP16Optimizer
from narg2p.optim.shard import shard_
from omegaconf import DictConfig

__all__ = [
    "FairseqOptimizer",
    "FP16Optimizer",
    "MemoryEfficientFP16Optimizer",
    "shard_",
]

(
    _build_optimizer,
    register_optimizer,
    OPTIMIZER_REGISTRY,
    OPTIMIZER_DATACLASS_REGISTRY,
) = registry.setup_registry("--optimizer", base_class=FairseqOptimizer, required=True)


def build_optimizer(cfg: DictConfig, params, *extra_args, **extra_kwargs):
    if all(isinstance(p, dict) for p in params):
        params = [t for p in params for t in p.values()]
    params = list(filter(lambda p: p.requires_grad, params))
    return _build_optimizer(cfg, params, *extra_args, **extra_kwargs)


# automatically import any Python files in the optim/ directory
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("_"):
        file_name = file[: file.find(".py")]
        importlib.import_module("narg2p.optim." + file_name)
