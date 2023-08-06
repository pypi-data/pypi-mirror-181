# PJAX

Do you just want probability distributions for JAX without all the added baggage of `tensorflow-probability` or `numpyro`?

Do you have some weird distribution not available in the above or `scipy.stats`?

Then `PJAX` is for you. Lightweight probability distributions using JAX backend. That's it.

```python
import jax
import jax.numpy as jnp
from pjax import distributions


a = jnp.asarray([4.3, 0.8])
b = jnp.asarray([1.2, 7.3])
dist = distributions.Gamma(a, b)

x = jnp.asarray([0.4, 0.5, 0.6, 0.7])
dist.log_pdf(x)

key = jax.random.PRNGKey(42)
dist.sample(key, shape=(100,))
```
