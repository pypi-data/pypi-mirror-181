from typing import Mapping, Sequence

import jax
import jax.scipy as jsp
from jax.tree_util import register_pytree_node_class

from ..support import PositiveReals, Support, UnitInterval
from .base import Distribution

# todo:
# InvGamma
# LogNormal
# NonCentralChiSquared
# Uniform


@register_pytree_node_class
class Beta(Distribution):
    def __init__(self, a: jax.Array, b: jax.Array) -> None:
        self.a = a
        self.b = b
        params = {"a": self.a, "b": self.b}
        super().__init__(params=params)

    @property
    def support(self) -> Support:
        return UnitInterval()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "a": PositiveReals(),
            "b": PositiveReals(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return self.a / (self.a + self.b)

    @property
    def variance(self) -> jax.Array:
        denom = (1 + self.a + self.b) * (self.a + self.b) ** 2
        return self.a * self.b / denom

    def _log_pdf(self, x: jax.Array) -> jax.Array:
        return jsp.stats.beta.logpdf(x, self.a, self.b)

    def _cdf(self, x: jax.Array) -> jax.Array:
        return jsp.special.betainc(self.a, self.b, x)

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        full_shape = tuple(shape) + tuple(self.batch_shape)
        return jax.random.beta(key, self.a, self.b, full_shape)


@register_pytree_node_class
class Gamma(Distribution):
    def __init__(self, a: jax.Array, b: jax.Array) -> None:
        self.a = a
        self.b = b
        params = {"a": self.a, "b": self.b}
        super().__init__(params=params)

    @property
    def support(self) -> Support:
        return PositiveReals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "a": PositiveReals(),
            "b": PositiveReals(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return self.a / self.b

    @property
    def variance(self) -> jax.Array:
        return self.a / self.b**2

    def _log_pdf(self, x: jax.Array) -> jax.Array:
        scale = 1 / self.b
        return jsp.stats.gamma.logpdf(x, self.a, scale=scale)

    def _cdf(self, x: jax.Array) -> jax.Array:
        return jsp.special.gammainc(self.a, self.b * x)

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        full_shape = tuple(shape) + tuple(self.batch_shape)
        z = jax.random.gamma(key, self.a, full_shape)
        return z / self.b
