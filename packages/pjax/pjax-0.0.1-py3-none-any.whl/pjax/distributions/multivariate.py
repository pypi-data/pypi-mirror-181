from typing import Mapping, Sequence

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax.tree_util import register_pytree_node_class

from ..support import CovarianceLike, Reals, Support
from .base import MultivariateDistribution


@register_pytree_node_class
class MultiNormal(MultivariateDistribution):
    def __init__(self, loc: jax.Array, scale: jax.Array) -> None:
        self.loc = loc
        self.scale = scale
        params = {"loc": self.loc, "scale": self.scale}
        super().__init__(params=params, dim=self.loc.shape[-1])

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "loc": Reals(),
            "scale": CovarianceLike(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return self.loc

    @property
    def variance(self) -> jax.Array:
        return self.scale

    @property
    def standard_deviation(self) -> jax.Array:
        return jnp.sqrt(jnp.diagonal(self.scale, 0, -1, -2))

    def log_pdf(self, x: jax.Array) -> jax.Array:
        val = jsp.stats.multivariate_normal.logpdf(x, self.loc, self.scale)
        return jnp.asarray(val)

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        z = jax.random.multivariate_normal(key, self.loc, self.scale, shape)
        return z
