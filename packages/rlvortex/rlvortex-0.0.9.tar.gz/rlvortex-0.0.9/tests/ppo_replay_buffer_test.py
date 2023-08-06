import gym
import torch
from rlvortex.envs.gym_wrapper.gym_envs import CartPoleEnv, MountainCarContinousEnv
from rlvortex.policy.ppo_policy import CategoricalActor, BaseCritic, BasePPOPolicy, GaussianActor
from rlvortex.policy.quick_build import mlp
from rlvortex.replay_buffer.ppo_replay_buffer import NpPPOReplayBuffer

if __name__ == "__main__":

    print("start collecting experience from CartPoleEnv (Categorical action space) with ppo policy ...")
    env = CartPoleEnv(render=True)
    replay_buffer: NpPPOReplayBuffer = NpPPOReplayBuffer(
        steps_per_env=50, observation_dim=env.observation_dim, action_dim=env.action_dim, random_sampler=True
    )
    device = torch.device("cuda:0")
    actor = CategoricalActor(net=mlp([*env.observation_dim, 32, env.action_n], torch.nn.ReLU),)
    critic = BaseCritic(net=mlp([*env.observation_dim, 32, 1], torch.nn.ReLU))
    policy = BasePPOPolicy(actor=actor, critic=critic, optimizer=torch.optim.Adam).to(device=device)
    o, info = env.reset()
    for _ in range(50):
        a, logp_a, v = policy.act(torch.as_tensor(o, dtype=torch.float32, device=device) - 1)
        a_h, logp_a_h, v_h = a.cpu().numpy(), logp_a.cpu().numpy(), v.cpu().numpy()
        o, r, d, info = env.step(a_h)
        env.render()
        replay_buffer.append_transitions(a_h, o, r, d, v_h, logp_a_h)
        if d:
            o, info = env.reset()
    env.close()
    replay_buffer.compute_returns(1, 0.9, 1.0)
    print(replay_buffer.done_buffer.reshape(1, 50))
    print(replay_buffer.reward_buffer.reshape(1, 50))
    print(replay_buffer.return_buffer.reshape(1, 50))
    print(replay_buffer.value_buffer.reshape(1, 50))

    for batch in replay_buffer.mini_batch_generator(10):
        print(batch)
