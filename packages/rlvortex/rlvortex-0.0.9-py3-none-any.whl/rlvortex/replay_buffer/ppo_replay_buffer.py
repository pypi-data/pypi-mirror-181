from typing import List, Tuple
import numpy as np
import torch
import torch
import torch
from torch.utils.data.sampler import (
    BatchSampler,
    SequentialSampler,
    SubsetRandomSampler,
)


class PPOReplayBuffer:
    def __init__(
        self,
        *,
        num_envs: int,
        steps_per_env: int,
        observation_dim: Tuple[int],
        action_dim: Tuple[int],
        random_sampler: bool = True,
    ):
        # record input parameters
        self.num_envs = num_envs
        self.steps_per_env = steps_per_env
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        self.random_sampler = random_sampler
        self.step = 0

    def append_transitions(self):
        if self.step >= self.steps_per_env:
            raise AssertionError("Replay buffer overflow")

    def clear(self):
        self.step = 0

    def mini_batch_generator(self, num_mini_batches):
        batch_size = self.num_envs * self.steps_per_env
        mini_batch_size = batch_size // num_mini_batches

        if self.sampler == "sequential":
            # For physics-based RL, each environment is already randomized. There is no value to doing random sampling
            # but a lot of CPU overhead during the PPO process. So, we can just switch to a sequential sampler instead
            subset = SequentialSampler(range(batch_size))
        elif self.sampler == "random":
            subset = SubsetRandomSampler(range(batch_size))

        batch = BatchSampler(subset, mini_batch_size, drop_last=True)
        return batch


class NpPPOReplayBuffer(PPOReplayBuffer):
    def __init__(
        self, *, steps_per_env, observation_dim, action_dim, random_sampler=False, num_envs: int = 1,
    ):
        super().__init__(
            num_envs=num_envs,
            steps_per_env=steps_per_env,
            observation_dim=observation_dim,
            action_dim=action_dim,
            random_sampler=random_sampler,
        )
        # core
        # abstract this part to parent class
        self.action_buffer = np.zeros((self.steps_per_env, self.num_envs, *self.action_dim))
        self.observation_buffer = np.zeros((self.steps_per_env, self.num_envs, *self.observation_dim))
        self.reward_buffer = np.zeros((self.steps_per_env, self.num_envs))
        # done_buffer is used to compute the returns and the advantages
        self.done_buffer = np.zeros((self.steps_per_env, self.num_envs))

        # ppo specific buffer
        self.advantage_buffer = np.zeros((self.steps_per_env, self.num_envs))
        self.return_buffer = np.zeros((self.steps_per_env, self.num_envs))
        self.value_buffer = np.zeros((self.steps_per_env, self.num_envs))
        self.actions_log_prob_buffer = np.zeros((self.steps_per_env, self.num_envs))

    def append_transitions(
        self,
        actions: np.array,
        observations: np.array,
        rewards: np.array,
        dones: np.array,
        values: np.array,
        actions_log_probs: np.array,
    ):
        super().append_transitions()
        self.action_buffer[self.step] = actions
        self.observation_buffer[self.step] = observations
        self.reward_buffer[self.step] = rewards
        self.done_buffer[self.step] = dones
        self.value_buffer[self.step] = values
        self.actions_log_prob_buffer[self.step] = actions_log_probs
        self.step += 1

    def compute_returns(self, last_value: float, gamma: float, lam: float):
        assert self.step == self.steps_per_env, "Replay buffer is not full"
        advantage = 0
        for step in reversed(range(self.steps_per_env)):
            if step == self.steps_per_env - 1:
                next_value = last_value
            else:
                next_value = self.value_buffer[step + 1]
            next_is_not_terminal = 1.0 - self.done_buffer[step]
            delta = self.reward_buffer[step] + next_is_not_terminal * gamma * next_value - self.value_buffer[step]
            advantage = delta + next_is_not_terminal * gamma * lam * advantage
            self.return_buffer[step] = advantage + self.value_buffer[step]
        # Compute and normalize the advantage_buffer
        self.advantage_buffer = self.return_buffer - self.value_buffer
        # self.advantage_buffer = (self.advantage_buffer - self.advantage_buffer.mean()) / (self.advantage_buffer.std() + 1e-8)

    def mini_batch_generator(self, num_mini_batches):
        sample_num = self.num_envs * self.steps_per_env
        mini_batch_size = max(1, sample_num // num_mini_batches)
        if self.random_sampler:
            subset = SubsetRandomSampler(range(sample_num))
        else:
            # For physics-based RL, each environment is already randomized. There is no value to doing random sampling
            # but a lot of CPU overhead during the PPO process. So, we can just switch to a sequential sampler instead
            subset = SequentialSampler(range(sample_num))
        mini_batch_indices = BatchSampler(subset, mini_batch_size, drop_last=True)
        return mini_batch_indices

    def tensor_data(self, device: torch.device):
        sample_num = self.num_envs * self.steps_per_env
        return (
            torch.as_tensor(self.action_buffer.reshape(sample_num, *self.action_dim), dtype=torch.float32, device=device),
            torch.as_tensor(
                self.observation_buffer.reshape(sample_num, *self.observation_dim), dtype=torch.float32, device=device
            ),
            torch.as_tensor(self.advantage_buffer.flatten(), dtype=torch.float32, device=device),
            torch.as_tensor(self.return_buffer.flatten(), dtype=torch.float32, device=device),
            torch.as_tensor(self.value_buffer.flatten(), dtype=torch.float32, device=device),
            torch.as_tensor(self.actions_log_prob_buffer.flatten(), dtype=torch.float32, device=device),
        )

