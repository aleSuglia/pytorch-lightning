# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities to describe gradients."""
from typing import Dict, Union

import torch
from torch.nn import Module


def grad_norm(module: Module, norm_type: Union[float, int, str]) -> Dict[str, float]:
    """Compute each parameter's gradient's norm and their overall norm.

    The overall norm is computed over all gradients together, as if they
    were concatenated into a single vector.

    Args:
        module: :class:`torch.nn.Module` to inspect.
        norm_type: The type of the used p-norm, cast to float if necessary.
            Can be ``'inf'`` for infinity norm.

    Return:
        norms: The dictionary of p-norms of each parameter's gradient and
            a special entry for the total p-norm of the gradients viewed
            as a single vector.
    """
    norm_type = float(norm_type)
    norms = {
        f"grad_{norm_type}_norm_{name}": p.grad.data.norm(norm_type).item()
        for name, p in module.named_parameters()
        if p.grad is not None
    }
    if norms:
        total_norm = torch.tensor(list(norms.values())).norm(norm_type).item()
        norms[f"grad_{norm_type}_norm_total"] = total_norm
        norms = {k: round(v, 4) for k, v in norms.items()}
    return norms
