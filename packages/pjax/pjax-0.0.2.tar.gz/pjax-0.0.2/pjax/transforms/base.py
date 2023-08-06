from __future__ import annotations

from abc import ABC
from typing import List, Mapping, Optional, Sequence, Tuple

import jax
from jax.tree_util import (
    PyTreeDef,
    register_pytree_node_class,
    tree_flatten,
    tree_unflatten,
)

from ..distributions.base import Distribution
from ..support import Reals, Support


@register_pytree_node_class
class Transform(Distribution, ABC):
    def __init__(
        self,
        distribution: Distribution,
        transform_params: Optional[Mapping[str, jax.Array]] = None,
    ) -> None:
        self.distribution = distribution
        self.transform_params: Mapping[str, jax.Array] = {}
        if transform_params is not None:
            self.transform_params = transform_params
        super().__init__(params=self.distribution.params)

    def tree_flatten(self) -> Tuple[List[jax.Array], PyTreeDef]:
        params = {
            "distribution": self.distribution,
            "transform": self.transform_params,
        }
        return tree_flatten(params)

    @classmethod
    def tree_unflatten(
        cls, treedef: PyTreeDef, leaves: Mapping[str, jax.Array]
    ) -> Transform:
        params = tree_unflatten(treedef, leaves)
        return cls(distribution=params["distribution"], **params["transform"])

    def forward(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("forward not implemented")

    def backward(self, y: jax.Array) -> jax.Array:
        raise NotImplementedError("backward not implemented")

    def log_det_jac(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("log_det_jac not implemented")

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        return self.distribution.bounds

    @property
    def mean(self) -> jax.Array:
        raise NotImplementedError("mean not implemented")

    @property
    def variance(self) -> jax.Array:
        raise NotImplementedError("variance not implemented")

    @property
    def standard_deviation(self) -> jax.Array:
        raise NotImplementedError("standard_deviation not implemented")

    def _log_pdf(self, x: jax.Array) -> jax.Array:
        p = self.distribution.log_pdf(self.backward(x))
        return p - self.log_det_jac(x)

    def _cdf(self, x: jax.Array) -> jax.Array:
        return self.distribution.cdf(self.backward(x))

    def _inv_cdf(self, p: jax.Array) -> jax.Array:
        return self.forward(self.distribution.inv_cdf(p))

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        return self.forward(self.distribution.sample(key, shape))
