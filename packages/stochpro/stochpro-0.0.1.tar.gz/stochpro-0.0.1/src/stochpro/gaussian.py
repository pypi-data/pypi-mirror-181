"""Gaussian Process.
"""

import numpy as np

from base import RandomProcess

from typing import Iterable


class GaussianProcess(RandomProcess):
    """Gaussian process.

    A stochastic process :math:`X = (X_t)_{t \\geq 0}` is a
    **Gaussian process** if for all :math:`n \\in \\mathbb{N}` and all
    time sequences :math:`t_1,\\ldots,t_n \\geq 0` with
    :math:`0 < t_1 < \\ldots < t_n` applies

    .. math::

        \\left( X_{t_1}, \\ldots, X_{t_n} \\right) \\sim \\mathcal{N}
        (m, \\Sigma)

    with :math:`m` a vector of expectations and :math:`\\Sigma` a
    covariance matrix, i.e.
    :math:`\\left( X_{t_1}, \\ldots, X_{t_n} \\right)` follows a
    :math:`n`-dimensional normal distribution.

    Notes
    -----
    For more information, see
    `Gaussian process <https://en.wikipedia.org/wiki/Gaussian_process>`_.

    Parameters
    ----------
    t : float, optional
        The right hand side of the time interval :math:`[0,t]`, by
        default 1.0.
    """

    def __init__(self, t: float = 1) -> None:
        super().__init__(t)

    def sample(self, n: int) -> np.array:
        return super().sample(n)

    def sample_at(self, times: Iterable[float]) -> np.array:
        return super().sample_at(times)
