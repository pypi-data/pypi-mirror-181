import abc
from collections import deque
import random
import torch
import numpy as np
from rlvortex.envs.base_env import BaseEnv


class BaseTrainer(abc.ABC):
    def __init__(self, *, env: BaseEnv, policy, steps_per_env: int, device_id: int, rd_seed: int) -> None:
        self.env = env
        self.steps_per_env = steps_per_env
        self.device_id = device_id
        self.device = torch.device(f"cuda:{device_id}") if device_id >= 0 else torch.device("cpu")
        self.policy = policy.to(self.device)
        self.ep_info_buffer = {
            "trainer/return": deque([0], maxlen=10),
            "trainer/length": deque([0], maxlen=10),
        }
        self.__set_random_seed(rd_seed)

    @property
    def observation_dim(self):
        return self.env.observation_dim

    @property
    def action_dim(self):
        return self.env.action_dim

    def __set_random_seed(self, rd_seed):
        self.env.set_random_seed(rd_seed)
        torch.manual_seed(rd_seed)
        torch.cuda.manual_seed_all(rd_seed)
        np.random.seed(rd_seed)
        random.seed(rd_seed)

    def train(self):
        raise NotImplementedError
