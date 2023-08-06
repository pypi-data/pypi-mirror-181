
import jax
import jax.numpy as jnp

@jax.jit
def gamma_metropolis_hastings(key, v_sample0, v, v_mean, v_std, post_θ, prior_k, cell_count):
    """
    Metropolis-hastings sample from gamma distributed signal. This is much cheaper
    an independent gamma at each step, though not as accurate.
    """

    perturb_key, accept_key = jax.random.split(key)

    # posterior gamma params
    α = v + prior_k * cell_count
    β = post_θ

    g0 = (v_sample0 * v_std) + v_mean # de-standardize

    # perturb to get proposal distribution
    g += 0.1 * α * jax.random.normal(perturb_key, g.shape)

    # accept/reject
    r = jnp.log(jax.random.uniform(accept_key, g.shape))
    h = (α - 1) * (jnp.log(g) - jnp.log(g0)) + β * (g0 - g)

    g = jax.lax.cond(
        r < h, lambda: g, lambda: g0)

    return (g - v_mean) / v_std

