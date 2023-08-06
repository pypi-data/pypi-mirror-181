import os
import torch
from rlvortex.envs.gym_wrapper.gym_envs import CartPoleEnv
from rlvortex.policy.ppo_policy import BaseCritic, BasePPOPolicy, CategoricalActor
from rlvortex.policy.quick_build import mlp
from rlvortex.trainer.ppo_trainer_sp import NativePPOTrainer
from rlvortex.utils import vlogger


if __name__ == "__main__":
    env = CartPoleEnv(render=False)
    ppo_trainer = NativePPOTrainer(
        env=env,
        policy=BasePPOPolicy(
            actor=CategoricalActor(net=mlp([*env.observation_dim, 32, 32, env.action_n], torch.nn.Tanh)),
            critic=BaseCritic(net=mlp([4, 32, 32, 1], torch.nn.Tanh)),
            optimizer=torch.optim.Adam,
            learning_rate=3e-4,
        ),
        device_id=-1,
        seed=314,
        steps_per_env=2048,
        learnint_iterations=80,
        num_batches_per_env=1,
        normalize_advantage=True,
        clip_ratio=0.2,
        dual_clip_ratio=None,
        gamma=0.99,
        lam=0.97,
        value_loss_coef=0.5,
        entropy_loss_coef=0.0,
        max_grad_norm=None,
        val_loss_clip=False,
        desired_kl=0.01,
        random_sampler=False,
        enable_tensorboard=True,
        save_freq=-1,
        log_type=vlogger.LogType.Screen,
    )
    ppo_trainer.train(50)
