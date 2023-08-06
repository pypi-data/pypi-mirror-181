import torch
from rlvortex.envs.gym_wrapper.gym_envs import CartPoleEnv, MountainCarContinousEnv
from rlvortex.policy.ppo_policy import CategoricalActor, BaseCritic, BasePPOPolicy, GaussianActor
from rlvortex.policy.quick_build import mlp


if __name__ == "__main__":
    # start testing BasePPOPolicy with CartPoleEnv (Categorical action space)

    env = CartPoleEnv(render=True)
    policy = BasePPOPolicy(
        actor=CategoricalActor(net=mlp([*env.observation_dim, 32, *env.action_dim], torch.nn.ReLU)),
        critic=BaseCritic(net=mlp([4, 32, 1], torch.nn.ReLU)),
        optimizer=torch.optim.Adam,
    )
    observation, info = env.reset()
    for _ in range(100):
        a, logp_a, v = policy.act(torch.as_tensor(observation, dtype=torch.float32))
        observation, reward, done, info = env.step(a.cpu().numpy())
        env.render()
        if done:
            observation, info = env.reset()
    env.close()
    # start testing BasePPOPolicy on Cuda with MountainCarContinous (Continous action space)
    env = MountainCarContinousEnv(render=True)
    device = torch.device("cuda:0")
    actor = GaussianActor(
        net=mlp([*env.observation_dim, 32, *env.action_dim], torch.nn.ReLU), init_log_std=torch.ones(*env.action_dim) * -0.5
    )
    critic = BaseCritic(net=mlp([*env.observation_dim, 32, 1], torch.nn.ReLU))
    policy = BasePPOPolicy(actor=actor, critic=critic, optimizer=torch.optim.Adam).to(device=device)
    observation, info = env.reset()
    for _ in range(100):
        a, logp_a, v = policy.act(torch.as_tensor(observation, dtype=torch.float32, device=device))
        observation, reward, done, info = env.step(a.cpu().numpy())
        env.render()
        if done:
            observation, info = env.reset()
    env.close()
