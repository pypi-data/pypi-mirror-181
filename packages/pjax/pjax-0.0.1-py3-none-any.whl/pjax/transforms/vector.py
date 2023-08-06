import jax
import jax.numpy as jnp
from jax.tree_util import register_pytree_node_class

from ..distributions.base import Distribution
from .base import Transform


@register_pytree_node_class
class Affine(Transform):
    def __init__(
        self, distribution: Distribution, loc: jax.Array, scale: jax.Array
    ) -> None:
        self.loc = loc
        self.scale = scale
        params = {"loc": self.loc, "scale": self.scale}
        super().__init__(distribution=distribution, transform_params=params)

    def forward(self, x: jax.Array) -> jax.Array:
        return self.loc + self.scale * x

    def backward(self, x: jax.Array) -> jax.Array:
        return (x - self.loc) / self.scale

    def log_det_jac(self, x: jax.Array) -> jax.Array:
        return jnp.log(self.scale)
