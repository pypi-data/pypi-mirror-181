from typing import Tuple
import gym
from rlvortex.envs.base_env import BaseEnv


class GymEnv(BaseEnv):
    def __init__(self, *, render: bool = False, seed: int = 314) -> None:
        super().__init__(seed=seed)
        self._render = render
        self.gym_env = None

    @property
    def observation_dim(self) -> Tuple[int]:
        return self.gym_env.observation_space.shape

    def reset(self):
        return self.gym_env.reset(return_info=True)

    def step(self, action: int):
        obs, r, d, t, cache = self.gym_env.step(action)
        return obs, r, d or t, {"truncated": t, "gym_cache": cache}

    def sample_action(self):
        return self.gym_env.action_space.sample()

    def render(self):
        assert self._render, "environment rendering is not enabled"
        self.gym_env.render()


class CartPoleEnv(GymEnv):
    def __init__(self, render: bool = False, seed: int = 314) -> None:
        super().__init__(render=render, seed=seed)
        if render:
            self.gym_env = gym.make("CartPole-v1", new_step_api=True, render_mode="human")
        else:
            self.gym_env = gym.make("CartPole-v1", new_step_api=True)

    def set_random_seed(self, rd_seed):
        self.seed = rd_seed
        self.gym_env.seed(self.seed)

    @property
    def action_dim(self) -> Tuple[int]:
        return ()

    @property
    def action_n(self) -> int:
        return self.gym_env.action_space.n


class MountainCarContinousEnv(GymEnv):
    def __init__(self, *, render: bool = False, seed: int = 314) -> None:
        super().__init__(render=render, seed=seed)
        if render:
            self.gym_env = gym.make("MountainCarContinuous-v0", new_step_api=True, render_mode="human")
        else:
            self.gym_env = gym.make("MountainCarContinuous-v0", new_step_api=True)

    @property
    def action_dim(self) -> Tuple[int]:
        return self.gym_env.action_space.shape
