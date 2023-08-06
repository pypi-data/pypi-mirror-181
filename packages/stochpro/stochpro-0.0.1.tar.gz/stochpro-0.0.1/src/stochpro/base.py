"""Base class.
"""
import numpy as np

from typing import Iterable

from abc import ABC
from abc import abstractmethod


class RandomProcess(ABC):
    """Base class for random time processes to be subclassed by all
    processes.

    Parameters
    ----------
    t : float, optional
        The right hand side of the time interval :math:`[0,t)`, by
        default 1.0.

    Methods
    -------
    sample
    sample_at
    """

    rng = np.random.default_rng()

    def __init__(self, t: float = 1.0) -> None:
        self.t = t

    @abstractmethod
    def sample(self, n: int) -> np.array:
        pass

    @abstractmethod
    def sample_at(self, times: Iterable[float]) -> np.array:
        pass
