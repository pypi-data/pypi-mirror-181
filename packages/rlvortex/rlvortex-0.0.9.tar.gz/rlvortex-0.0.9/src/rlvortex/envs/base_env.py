import abc
import random
from typing import Tuple
import torch
import numpy as np


class BaseEnv(abc.ABC):
    def __init__(self, *, seed: int = 314) -> None:
        """
        args: 
        device_id: int, if device_id == -1, use numpy, else use torch for cuda computation
        """
        self.seed = seed

    def set_random_seed(self):
        raise NotImplementedError

    @property
    def observation_dim(self):
        raise NotImplementedError

    @property
    def action_dim(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def sample_action(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def close(self):
        pass


class BaseCudaEnv(BaseEnv):
    def __init__(self, *, eposide_len: int, device_id: int, seed: int = 314) -> None:
        super().__init__(eposide_len=eposide_len, seed=seed)
        self.device_id = device_id

