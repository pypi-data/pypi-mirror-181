import jax
import jax.numpy as jnp
from jax.tree_util import register_pytree_node_class

from .base import Transform


@register_pytree_node_class
class Exponential(Transform):
    def forward(self, x: jax.Array) -> jax.Array:
        return jnp.exp(x)

    def backward(self, x: jax.Array) -> jax.Array:
        return jnp.log(x)

    def log_det_jac(self, x: jax.Array) -> jax.Array:
        return x


@register_pytree_node_class
class Reciprocal(Transform):
    def forward(self, x: jax.Array) -> jax.Array:
        return 1 / x

    def backward(self, x: jax.Array) -> jax.Array:
        return 1 / x

    def log_det_jac(self, x: jax.Array) -> jax.Array:
        return -2 * jnp.log(jnp.abs(x))
