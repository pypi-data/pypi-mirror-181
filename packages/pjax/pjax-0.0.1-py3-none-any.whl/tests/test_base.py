import jax
import jax.numpy as jnp

from pjax import distributions


def test_simple() -> None:
    a = jnp.asarray([4.3, 0.8])
    b = jnp.asarray([1.2, 7.3])
    dist = distributions.Gamma(a, b)

    x = jnp.asarray([0.4, 0.5, 0.6, 0.7])
    dist.log_pdf(x[..., None])

    key = jax.random.PRNGKey(42)
    dist.sample(key, shape=(1000, 2))

    assert True
