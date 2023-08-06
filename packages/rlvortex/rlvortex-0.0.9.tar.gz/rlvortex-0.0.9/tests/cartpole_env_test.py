import gym
import torch
from rlvortex.envs.gym_wrapper.gym_envs import CartPoleEnv, MountainCarContinousEnv
from rlvortex.policy.ppo_policy import BaseActor, BaseCritic, BasePPOPolicy
from rlvortex.policy.quick_build import mlp


if __name__ == "__main__":
    # CartPoleEnv
    print("start testing CartPoleEnv for 100 steps")
    env = CartPoleEnv(render=True)
    print("observation_dim:", env.observation_dim)
    print("action_dim:", env.action_dim)
    print("reset:", env.reset())
    print("sample_action:", env.sample_action())
    print("step:", env.step(env.sample_action()))
    observation, info = env.reset()
    for _ in range(100):
        observation, reward, done, info = env.step(env.sample_action())
        env.render()
        if done:
            observation, info = env.reset()
    env.close()
    # MountainCarContinousEnv
    print("start testing MountainCarContinousEnv for 100 steps")
    env = MountainCarContinousEnv(render=True)
    observation, info = env.reset()
    for _ in range(100):
        observation, reward, done, info = env.step(env.sample_action())
        env.render()
        if done:
            observation, info = env.reset()
    env.close()
