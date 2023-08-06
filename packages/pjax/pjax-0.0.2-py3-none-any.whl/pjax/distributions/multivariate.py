from typing import Mapping, Sequence

import jax
import jax.numpy as jnp
import jax.scipy as jsp
from jax.scipy.special import gammaln
from jax.tree_util import register_pytree_node_class

from ..support import CovarianceLike, PositiveReals, Reals, Support
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

    def _log_pdf(self, x: jax.Array) -> jax.Array:
        val = jsp.stats.multivariate_normal.logpdf(x, self.loc, self.scale)
        return jnp.asarray(val)

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        full_shape = tuple(shape) + tuple(self.batch_shape)
        z = jax.random.multivariate_normal(key, self.loc, self.scale, full_shape)
        return z


@register_pytree_node_class
class MultiStudentT(MultivariateDistribution):
    def __init__(self, dof: jax.Array, loc: jax.Array, scale: jax.Array) -> None:
        self.dof = dof
        self.loc = loc
        self.scale = scale
        dim = self.loc.shape[-1]
        self.log_pdf_constant = (
            gammaln(0.5 * self.dof)
            - gammaln(0.5 * (dim + self.dof))
            + 0.5 * dim * jnp.log(self.dof * jnp.pi)
            + 0.5 * jnp.linalg.slogdet(self.scale)[0]
        )
        self.inv_scale = jnp.linalg.pinv(self.scale)
        params = {"dof": self.dof, "loc": self.loc, "scale": self.scale}
        super().__init__(params=params, dim=dim)

    @property
    def support(self) -> Support:
        return Reals()

    @property
    def bounds(self) -> Mapping[str, Support]:
        bounds = {
            "dof": PositiveReals(),
            "loc": Reals(),
            "scale": CovarianceLike(),
        }
        return bounds

    @property
    def mean(self) -> jax.Array:
        return self.loc

    @property
    def variance(self) -> jax.Array:
        return self.dof * self.scale / (self.dof - 2)

    @property
    def standard_deviation(self) -> jax.Array:
        return jnp.sqrt(jnp.diagonal(self.variance, 0, -1, -2))

    def _log_pdf(self, x: jax.Array) -> jax.Array:
        z = x - self.loc
        z = jnp.einsum("...i,...ij,...j->...", z, self.inv_scale, z)
        p = -(self.dof + self.dim) * jnp.log1p(z / self.dof) / 2
        return jnp.asarray(p - self.log_pdf_constant)

    def sample(
        self, key: jax.random.PRNGKeyArray, shape: Sequence[int] = ()
    ) -> jax.Array:
        full_shape = tuple(shape) + tuple(self.batch_shape)
        norm_sim = jax.random.multivariate_normal(key, 0, self.scale, full_shape)
        chi2_sim = 2 * jax.random.gamma(key, self.dof / 2, full_shape)
        chi2_sim = jnp.sqrt(chi2_sim / self.dof)
        sim = self.loc + norm_sim / chi2_sim[..., None]
        return sim
