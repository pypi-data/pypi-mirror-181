from typing import Mapping, Sequence

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax.tree_util import register_pytree_node_class

from ..support import PositiveReals, Reals, Support
from .base import Distribution

# todo:
# Normal
# SkewNormal


@register_pytree_node_class
class Normal(Distribution):
    def __init__(self, mu: jax.Array, sigma: jax.Array) -> None:
        self.mu = mu
        self.sigma = sigma
        params = {"mu": self.mu, "sigma": self.sigma}
        super().__init__(params=params)

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "mu": Reals(),
            "sigma": PositiveReals(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return self.mu

    @property
    def variance(self) -> jax.Array:
        return self.sigma**2

    @property
    def standard_deviation(self) -> jax.Array:
        return self.sigma

    def log_pdf(self, x: jax.Array) -> jax.Array:
        return jsp.stats.norm.logpdf(x, self.mu, self.sigma)

    def cdf(self, x: jax.Array) -> jax.Array:
        return jsp.stats.norm.cdf(x, self.mu, self.sigma)

    def inv_cdf(self, p: jax.Array) -> jax.Array:
        return jsp.stats.norm.ppf(p, self.mu, self.sigma)

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        z = jax.random.normal(key, shape)
        return self.mu + self.sigma * z


@register_pytree_node_class
class StudentT(Distribution):
    def __init__(self, df: jax.Array, mu: jax.Array, sigma: jax.Array) -> None:
        self.df = df
        self.mu = mu
        self.sigma = sigma
        params = {"df": self.df, "mu": self.mu, "sigma": self.sigma}
        super().__init__(params=params)

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "df": PositiveReals(),
            "mu": Reals(),
            "sigma": PositiveReals(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return jnp.where(self.df > 1, self.mu, jnp.nan)

    @property
    def variance(self) -> jax.Array:
        v = self.df * self.sigma**2 / (self.df - 2)
        return jnp.where(self.df > 2, v, jnp.nan)

    def log_pdf(self, x: jax.Array) -> jax.Array:
        return jsp.stats.t.logpdf(x, self.df, self.mu, self.sigma)

    def cdf(self, x: jax.Array) -> jax.Array:
        z = (x - self.mu) / self.sigma
        z_1 = self.df / (self.df + z**2)
        z_2 = z**2 / (self.df + z**2)
        p_1 = jsp.special.betainc(0.5 * self.df, 0.5, z_1)
        p_2 = 1 + jsp.special.betainc(0.5, 0.5 * self.df, z_2)
        return 0.5 * jnp.where(x <= 0, p_1, p_2)

    def inv_cdf(self, p: jax.Array) -> jax.Array:
        raise NotImplementedError("betaincinv not implemented")

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        z = jax.random.t(key, self.df, shape)
        return self.mu + self.sigma * z


@register_pytree_node_class
class Cauchy(Distribution):
    def __init__(self, loc: jax.Array, scale: jax.Array) -> None:
        self.loc = loc
        self.scale = scale
        params = {"loc": self.loc, "scale": self.scale}
        super().__init__(params=params)

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "loc": Reals(),
            "scale": PositiveReals(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return jnp.asarray(jnp.nan)

    @property
    def variance(self) -> jax.Array:
        return jnp.asarray(jnp.nan)

    def log_pdf(self, x: jax.Array) -> jax.Array:
        return jsp.stats.cauchy.logpdf(x, self.loc, self.scale)

    def cdf(self, x: jax.Array) -> jax.Array:
        z = (x - self.loc) / self.scale
        return 0.5 + jnp.arctan(z) / jnp.pi

    def inv_cdf(self, p: jax.Array) -> jax.Array:
        z = jnp.tan(jnp.pi * (p - 0.5))
        return self.loc + self.scale * z

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        z = jax.random.cauchy(key, shape)
        return self.loc + self.scale * z


@register_pytree_node_class
class SkewNormal(Distribution):
    def __init__(self, a: jax.Array, loc: jax.Array, scale: jax.Array) -> None:
        self.a = a
        self.loc = loc
        self.scale = scale
        params = {"a": self.a, "loc": self.loc, "scale": self.scale}
        super().__init__(params=params)

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "a": Reals(),
            "loc": Reals(),
            "scale": PositiveReals(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        g = self.a * self.scale / jnp.sqrt(1 + self.a**2)
        return self.loc + jnp.sqrt(2 / jnp.pi) * g

    @property
    def variance(self) -> jax.Array:
        g = 2 * self.a**2 / (1 + self.a**2)
        return (1 - g / jnp.pi) * self.scale**2

    def log_pdf(self, x: jax.Array) -> jax.Array:
        z = (x - self.loc) / self.scale
        p = jsp.stats.norm.logpdf(x, self.loc, self.scale)
        p = p + jsp.stats.norm.logcdf(self.a * z)
        return p + jnp.log(2)

    def cdf(self, x: jax.Array) -> jax.Array:
        raise NotImplementedError("owens_t not implemented")

    def inv_cdf(self, p: jax.Array) -> jax.Array:
        raise NotImplementedError("inv_cdf not implemented")

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        z_1, z_2 = jax.random.normal(key, (2,) + tuple(shape))
        z = (self.a * jnp.abs(z_1) + z_2) / jnp.sqrt(1 + self.a**2)
        return jnp.asarray(self.loc + self.scale * z)
