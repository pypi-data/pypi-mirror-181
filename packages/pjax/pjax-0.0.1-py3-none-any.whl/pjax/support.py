from abc import ABC, abstractmethod

import jax
import jax.numpy as jnp
from jax.scipy.special import expit


class Support(ABC):
    @abstractmethod
    def check(self, val: jax.Array) -> jax.Array:
        pass

    @abstractmethod
    def cast(self, val: jax.Array) -> jax.Array:
        pass


class Reals(Support):
    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        return val


class PositiveReals(Support):
    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val) & (0 <= val)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        return jnp.exp(val)


class UnitInterval(Support):
    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val) & (0 <= val) & (val <= 1)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        return expit(val)


class BoundedContinuous(Support):
    def __init__(self, lower: float, upper: float) -> None:
        self.lower = lower
        self.upper = upper

    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val) & (self.lower <= val) & (val <= self.upper)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        return self.lower + (self.upper - self.lower) * expit(val)


class Integers(Support):
    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val) & jnp.issubdtype(val, jnp.integer)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        return val.astype(jnp.int32)


class PositiveIntegers(Support):
    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val) & jnp.issubdtype(val, jnp.integer)
        valid = valid & (0 <= val)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        new_val = jnp.clip(val.astype(jnp.int32), 0)
        return jnp.asarray(new_val)


class BoundedIntegers(Support):
    def __init__(self, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper

    def check(self, val: jax.Array) -> jax.Array:
        valid = jnp.isfinite(val) & jnp.issubdtype(val, jnp.integer)
        valid = valid & (self.lower <= val) & (val <= self.upper)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        new_val = jnp.clip(val.astype(jnp.int32), self.lower, self.upper)
        return jnp.asarray(new_val)


class UnitSimplex(Support):
    def check(self, val: jax.Array) -> jax.Array:
        if val.ndim < 1:
            raise ValueError("vector support requires at least 1D array")
        norm = jnp.sum(val, axis=-1, keepdims=True)
        valid = jnp.isfinite(val) & (0 <= val) & (val <= 1)
        valid = valid & jnp.isclose(norm, 1)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        new_val = jax.nn.softmax(val, axis=-1)
        return jnp.asarray(new_val)


class UnitVector(Support):
    def check(self, val: jax.Array) -> jax.Array:
        if val.ndim < 1:
            raise ValueError("vector support requires at least 1D array")
        norm = jnp.sum(jnp.abs(val) ** 2, axis=-1, keepdims=True)
        valid = jnp.isfinite(val) & jnp.isclose(norm, 1)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        norm = jnp.sum(jnp.abs(val) ** 2, axis=-1, keepdims=True)
        return jnp.asarray(val / norm)


class CovarianceLike(Support):
    def check(self, val: jax.Array) -> jax.Array:
        if val.ndim < 2:
            raise ValueError("matrix support requires at least 2D array")
        if val.shape[-1] != val.shape[-2]:
            raise ValueError("matrix is not square")
        chol = jnp.linalg.cholesky(val)
        valid = jnp.all(jnp.isfinite(chol), axis=(-1, -2), keepdims=True)
        valid = valid & jnp.isfinite(val)
        valid = valid & jnp.isclose(jnp.swapaxes(val, -1, -2), val)
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        if val.ndim < 2:
            raise ValueError("matrix support requires at least 2D array")
        if val.shape[-1] != val.shape[-2]:
            raise ValueError("matrix is not square")
        new_val = jnp.einsum("...ki,...kj->...ij", val, val)
        return jnp.asarray(new_val)


class CorrelationLike(Support):
    def check(self, val: jax.Array) -> jax.Array:
        if val.ndim < 2:
            raise ValueError("matrix support requires at least 2D array")
        if val.shape[-1] != val.shape[-2]:
            raise ValueError("matrix is not square")
        chol = jnp.linalg.cholesky(val)
        valid = jnp.all(jnp.isfinite(chol), axis=(-1, -2), keepdims=True)
        valid = valid & jnp.isfinite(val) & (-1 <= val) & (val <= 1)
        valid = valid & jnp.isclose(jnp.swapaxes(val, -1, -2), val)
        valid = valid & jnp.isclose(jnp.diagonal(val, 0, -1, -2), 1)[..., None]
        return jnp.asarray(valid)

    def cast(self, val: jax.Array) -> jax.Array:
        if val.ndim < 2:
            raise ValueError("matrix support requires at least 2D array")
        if val.shape[-1] != val.shape[-2]:
            raise ValueError("matrix is not square")
        norm = jnp.sqrt(jnp.sum(jnp.abs(val) ** 2, axis=-2, keepdims=True))
        new_val = val / norm
        new_val = jnp.einsum("...ki,...kj->...ij", new_val, new_val)
        return jnp.asarray(new_val)
