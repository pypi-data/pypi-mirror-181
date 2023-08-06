"""Base agent class."""

from abc import ABC, abstractmethod
from typing import Any

import gym
import numpy as np


class BaseAgent(ABC):
    """Agent base class."""

    @abstractmethod
    def predict(self, obs: np.ndarray, env: gym.Env, **kwargs: Any) -> int:
        """Abstract predict method.

        :param obs: observation.
        :param env: environment.
        :raises NotImplementedError: subclasses should have a predict method.
        :return: action.
        """
        raise NotImplementedError
