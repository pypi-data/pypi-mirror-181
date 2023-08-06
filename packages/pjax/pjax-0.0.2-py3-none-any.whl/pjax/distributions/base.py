from __future__ import annotations

from abc import ABC
from typing import List, Mapping, Sequence, Tuple

import jax
import jax.numpy as jnp
from jax.tree_util import (
    PyTreeDef,
    register_pytree_node_class,
    tree_flatten,
    tree_unflatten,
)

from ..support import Reals, Support

JAX_MAP = Mapping[str, jax.Array]
TEST_VALUE: float = 1.0


@register_pytree_node_class
class Distribution(ABC):
    def __init__(self, params: JAX_MAP) -> None:
        self.params = params
        self.batch_shape = self._get_batch_shape()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def _get_batch_shape(self) -> Sequence[int]:
        # something of a hack, but we determine batch_shape by evaluating
        # the log_pdf at a scalar value
        x = self.support.cast(jnp.asarray(TEST_VALUE))
        return self._log_pdf(x).shape

    def expand(self, x: jax.Array) -> jax.Array:
        expand_shape = range(-len(self.batch_shape), 0)
        return jnp.expand_dims(x, expand_shape)

    def tree_flatten(self) -> Tuple[List[jax.Array], PyTreeDef]:
        return tree_flatten(self.params)

    @classmethod
    def tree_unflatten(cls, treedef: PyTreeDef, leaves: JAX_MAP) -> Distribution:
        params = tree_unflatten(treedef, leaves)
        return cls(**params)

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

    def _log_pdf(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("_log_pdf not implemented")

    def log_pdf(self, x: jax.Array) -> jax.Array:
        return self._log_pdf(self.expand(x))

    def pdf(self, x: jax.Array) -> jax.Array:
        return jnp.exp(self.log_pdf(x))

    def _cdf(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("_cdf not implemented")

    def cdf(self, x: jax.Array) -> jax.Array:
        return self._cdf(self.expand(x))

    def _inv_cdf(self, p: jax.Array) -> jax.Array:
        raise NotImplementedError("inv_cdf not implemented")

    def inv_cdf(self, p: jax.Array) -> jax.Array:
        return self._cdf(self.expand(p))

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        full_shape = tuple(shape) + tuple(self.batch_shape)
        p = jax.random.uniform(key, full_shape)
        sim = self.inv_cdf(p)
        return sim


class MultivariateDistribution(Distribution, ABC):
    def __init__(self, params: JAX_MAP, dim: int) -> None:
        self.dim = dim
        super().__init__(params)

    def _get_batch_shape(self) -> Sequence[int]:
        # something of a hack, but we determine batch_shape by evaluating
        # the log_pdf at a scalar value
        x = self.support.cast(jnp.repeat(TEST_VALUE, self.dim))
        return self._log_pdf(x).shape

    def expand(self, x: jax.Array) -> jax.Array:
        expand_shape = range(-len(self.batch_shape) - 1, -1)
        return jnp.expand_dims(x, expand_shape)
