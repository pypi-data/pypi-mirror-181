from __future__ import annotations

from abc import ABC
from typing import List, Mapping, Sequence, Tuple

import jax
import jax.numpy as jnp
from jax.tree_util import register_pytree_node_class, tree_flatten, tree_unflatten

from ..support import Reals, Support


@register_pytree_node_class
class Distribution(ABC):
    def __init__(self, params: Mapping[str, jax.Array]) -> None:
        self.params = params

    def tree_flatten(self) -> Tuple[List[jax.Array], jax.tree_util.PyTreeDef]:
        return tree_flatten(self.params)

    @classmethod
    def tree_unflatten(
        cls, treedef: jax.tree_util.PyTreeDef, leaves: Mapping[str, jax.Array]
    ) -> Distribution:
        params = tree_unflatten(treedef, leaves)
        return cls(**params)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        raise NotImplementedError("bounds not implemented")

    def check_bounds(self) -> None:
        for key, val in self.params.items():
            if not self.bounds[key].check(val).all():
                raise ValueError(f"{key} out of bounds")

    @property
    def mean(self) -> jax.Array:
        raise NotImplementedError("mean not implemented")

    @property
    def variance(self) -> jax.Array:
        raise NotImplementedError("variance not implemented")

    @property
    def standard_deviation(self) -> jax.Array:
        return jnp.sqrt(self.variance)

    def log_pdf(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("logpdf not implemented")

    def pdf(self, x: jax.Array) -> jax.Array:
        return jnp.exp(self.log_pdf(x))

    def cdf(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("cdf not implemented")

    def inv_cdf(self, p: jax.Array) -> jax.Array:
        raise NotImplementedError("inv_cdf not implemented")

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        raise NotImplementedError("sample not implemented")


class MultivariateDistribution(Distribution, ABC):
    def __init__(self, params: Mapping[str, jax.Array], dim: int) -> None:
        self.dim = dim
        super().__init__(params)
