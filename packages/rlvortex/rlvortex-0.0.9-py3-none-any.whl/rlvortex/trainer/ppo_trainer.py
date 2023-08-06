import os
import logging
from typing import List
from datetime import datetime
import numpy as np
import torch
from torch import optim
from torch.utils.tensorboard import SummaryWriter
from collections import namedtuple
from rlvortex.replay_buffer.ppo_replay_buffer import NpPPOReplayBuffer
from rlvortex.policy.ppo_policy import BasePPOPolicy
from rlvortex.trainer.base_trainer import BaseTrainer
from rlvortex.utils import vlogger
from rlvortex.utils.trainer_utils import v_debug

TrainerMonitorTale = namedtuple(
    "TrainMonitorTale",
    ["start_time", "start_time_str", "trainer_name", "trainer_path", "tensorboard_path", "save_path", "log_path"],
)


class NativePPOTrainer(BaseTrainer):
    def __init__(
        self,
        *,
        env,
        policy: BasePPOPolicy,
        device_id: int,
        seed: int = 314,
        steps_per_env=32,
        learnint_iterations=8,
        num_batches_per_env: int = 2,
        lr_range: List[float] = [3e-4, 1e-4],
        normalize_advantage: bool = True,
        clip_ratio: float = 0.2,
        dual_clip_ratio: float = None,
        gamma: float = 0.998,
        lam: float = 0.95,
        value_loss_coef=1.0,
        entropy_loss_coef=0.0,
        max_grad_norm=2.0,
        val_loss_clip=True,
        desired_kl=0.008,
        random_sampler: bool = False,
        trainer_dir: os.path = os.path.join(os.getcwd(), "trainers"),
        enable_tensorboard: bool = False,
        save_freq: int = -1,  # if save_freg == -1, then disable save, if save_freq == 0, then save at the end of training,otherwise save every save_freq epochs
        log_type: vlogger.LogType = vlogger.LogType.Screen,
        comment: str = "",
    ) -> None:
        super().__init__(env=env, policy=policy, steps_per_env=steps_per_env, device_id=device_id, rd_seed=seed)
        # store input parameters
        self.learning_iterations = learnint_iterations
        self.num_batches_per_env = num_batches_per_env
        self.lr_range = lr_range
        self.normalize_advantage = normalize_advantage
        self.clip_ratio = clip_ratio
        self.dual_clip_ratio = dual_clip_ratio
        self.gamma = gamma
        self.lam = lam
        self.val_loss_coef = value_loss_coef
        self.entropy_loss_coef = entropy_loss_coef
        self.learning_rate = self.policy.learning_rate
        self.max_grad_norm = max_grad_norm
        self.val_loss_clip = val_loss_clip
        self.desired_kl = desired_kl
        self.random_sampler = random_sampler
        self.train_dir = trainer_dir
        self.save_freq = save_freq
        self.enable_tensorboard = enable_tensorboard
        self.log_type = log_type
        self.comment = comment
        # init variables
        self.replay_buffer: NpPPOReplayBuffer = NpPPOReplayBuffer(
            num_envs=1,
            steps_per_env=self.steps_per_env,
            observation_dim=self.env.observation_dim,
            action_dim=self.env.action_dim,
            random_sampler=self.random_sampler,
        )
        self.optimizer = optim.Adam(self.policy.parameters(), lr=self.learning_rate)
        # log and save
        start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        trainer_name = f"ppo_trainer_{start_time_str}_cmt_{self.comment}"
        trainer_path = os.path.join(self.train_dir, trainer_name)
        self.trainer_montior_table = TrainerMonitorTale(
            start_time=start_time,
            start_time_str=start_time_str,
            trainer_name=trainer_name,
            trainer_path=os.path.join(trainer_path),
            save_path=os.path.join(trainer_path, "models"),
            tensorboard_path=os.path.join(trainer_path, "runs"),
            log_path=os.path.join(trainer_path, "trainer.log"),
        )
        self.__gen_trainer_dirs()
        self.logger = vlogger.VLogger(log_type=self.log_type, log_path=self.trainer_montior_table.log_path)
        self.logger.info_dict(self.params)

    def __gen_trainer_dirs(self):
        if self.save_freq > 0 and not os.path.exists(self.trainer_montior_table.save_path):
            os.mkdir(self.trainer_montior_table.save_path)
        if self.enable_tensorboard and not os.path.exists(self.trainer_montior_table.tensorboard_path):
            self._tb_writer = SummaryWriter(
                self.trainer_montior_table.tensorboard_path, comment=self.trainer_montior_table.trainer_name
            )

    def train(self, epochs: int):
        o, _ = self.env.reset()
        episode_len = 0
        episode_return = 0
        for epoch in range(epochs):
            for t in range(self.steps_per_env):
                a, logp_a, v = self.policy.act(
                    torch.as_tensor(o, dtype=torch.float32, device=self.device)
                )  # in torch.Tensor,no gradient computed
                next_o, r, d, cache = self.env.step(a.cpu().numpy())
                episode_return += r
                episode_len += 1
                self.replay_buffer.append_transitions(a.cpu().numpy(), o, r, d, v.cpu().numpy(), logp_a.cpu().numpy())
                if d:
                    self.ep_info_buffer["trainer/return"].append(episode_return)
                    self.ep_info_buffer["trainer/length"].append(episode_len)
                    (next_o, _), episode_return, episode_len = self.env.reset(), 0, 0
                o = next_o
            _, _, last_value = self.policy.act(torch.as_tensor(o, device=self.device))
            self.replay_buffer.compute_returns(last_value.cpu().numpy(), self.gamma, self.lam)
            # self.replay_buffer.compute_returns(0, self.gamma, self.lam)
            print(
                f"epoch: {epoch}, return: {np.mean(self.ep_info_buffer['trainer/return'])}, max: {np.max(self.ep_info_buffer['trainer/return'])}, min: {np.min(self.ep_info_buffer['trainer/return'])}, std: {np.std(self.ep_info_buffer['trainer/return'])}"
            )
            self.__spinning_up_update_policy()
            # self.__update_policy()
            self.replay_buffer.clear()

    def clear(self):
        self.envs.destroy()
        self.net = None
        del self.net

    @property
    def params(self):
        return {
            "gamma": self.gamma,
            "lam": self.lam,
            "steps_per_env": self.steps_per_env,
            "value_loss_coef": self.val_loss_coef,
            "entropy_loss_coef": self.entropy_loss_coef,
            "net_lr": self.learning_rate,
            "max_grad_norm": self.max_grad_norm,
            "use_clipped_value_loss": self.val_loss_clip,
            "desired_kl": self.desired_kl,
            "sampler": self.random_sampler,
            "save_freq": self.save_freq,
        }

    def __update_policy(self):
        batches_indices = self.replay_buffer.mini_batch_generator(self.num_batches_per_env)
        act_data, obs_data, adv_data, ret_data, val_data, act_logp_data, = self.replay_buffer.tensor_data(self.device)
        for _ in range(self.learning_iterations):
            for indices in batches_indices:
                old_act = act_data[indices]
                old_obs = obs_data[indices]
                old_val = val_data[indices]
                old_act_logp = act_logp_data[indices]
                ret = ret_data[indices]
                adv = adv_data[indices]

                # normalize advantages
                # adv = (adv - adv.mean()) / (adv.std() + 1e-8)
                # compute values for policy and value loss
                act_logp, val, entropy = self.policy(old_act, old_obs)

                # compute pi loss
                policy_ratio = torch.exp(act_logp - old_act_logp)
                # perform normal ppo clipping
                clipped_ratio = torch.clamp(policy_ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
                pi_losses = -torch.min(policy_ratio * adv, clipped_ratio * adv)
                # perform dual clipping: https://arxiv.org/pdf/1912.09729.pdf
                if self.dual_clip_ratio:
                    dual_clipped_pi_losses = -self._dual_clip * adv
                    pi_loss = torch.where(adv < 0, dual_clipped_pi_losses, pi_losses).mean()
                else:
                    pi_loss = pi_losses.mean()
                # compute value loss
                """
                # value loss clip: https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/ -> Value Function Loss Clipping (ppo2/model.py#L68-L75)

                Value Function Loss Clipping (ppo2/model.py#L68-L75) Code-level Optimizations
                PPO clips the value function like the PPO’s clipped surrogate objective. Given the V_{targ} = returns = advantages + values, PPO fits the the value network by minimizing the following loss:

                LV=max[(Vθt−Vtarg)2,(clip(Vθt,Vθt−1−ε,Vθt−1+ε)−Vtarg)2]
                Engstrom, Ilyas, et al., (2020) find no evidence that the value function loss clipping helps with the performance. Andrychowicz, et al. (2021) suggest value function loss clipping even hurts performance (decision C13, figure 43).
                We implemented this detail because this work is more about high-fidelity reproduction of prior results.
                """
                if self.val_loss_clip:
                    values_clipped = old_val + (val - old_val).clamp(-self.clip_ratio, self.clip_ratio)
                    val_losses = (val - ret).pow(2)
                    clipped_val_losses = (values_clipped - ret).pow(2)
                    value_loss = torch.max(val_losses, clipped_val_losses).mean()
                else:
                    value_loss = (val - ret).pow(2).mean()

                # compute total loss
                loss = pi_loss + self.val_loss_coef * value_loss - self.entropy_loss_coef * entropy
                # v_debug()

                # compute kl divergence and adaptively adjust learning rate
                if self.desired_kl:
                    """
                    https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/
                    approxkl: the approximate Kullback–Leibler divergence, measured by (-logratio).mean(), which corresponds to the k1 estimator in John Schulman’s blog post on approximating KL divergence. This blog post also suggests using an alternative estimator ((ratio - 1) - logratio).mean(), which is unbiased and has less variance.

                    """
                    log_ratio = (act_logp - old_act_logp).mean()
                    if log_ratio > self.desired_kl * 1.5:
                        break
                    # approx_kl_div = torch.mean((torch.exp(log_ratio) - 1) - log_ratio)
                    # learning_rate = self.policy.learning_rate
                    # if approx_kl_div > self.desired_kl * 2.0:
                    #     learning_rate = max(self.lr_range[0], learning_rate / 1.5)
                    # elif approx_kl_div < self.desired_kl / 2.0 and approx_kl_div > 0.0:
                    #     learning_rate = min(self.lr_range[1], learning_rate * 1.5)
                    # self.policy.update_learning_rate(learning_rate)
                # compute gradient and do update step
                self.policy.optimizer.zero_grad()
                loss.backward()
                # Clip grad norm
                if self.max_grad_norm:
                    torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
                self.policy.optimizer.step()

    def __spinning_up_update_policy(self):
        batches_indices = self.replay_buffer.mini_batch_generator(self.num_batches_per_env)
        act_data, obs_data, adv_data, ret_data, _, act_logp_data, = self.replay_buffer.tensor_data(self.device)
        # pi update
        for _ in range(80):
            for indices in batches_indices:
                old_act = act_data[indices]
                old_obs = obs_data[indices]
                old_act_logp = act_logp_data[indices]
                ret = ret_data[indices]
                adv = adv_data[indices]
                adv = (adv - adv.mean()) / (adv.std() + 1e-8)

                act_logp, val, entropy = self.policy(old_act, old_obs)
                # compute pi loss
                ratio = torch.exp(act_logp - old_act_logp)
                clip_adv = torch.clamp(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio) * adv
                # perform normal ppo clipping
                clipped_ratio = torch.clamp(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
                pi_loss = -(torch.min(ratio * adv, clip_adv)).mean()

                # compute kl divergence and adaptively adjust learning rate
                if self.desired_kl:
                    approx_kl = (old_act_logp - act_logp).mean()
                    if approx_kl > self.desired_kl * 1.5:
                        break

                self.policy.actor_optimizer.zero_grad()
                pi_loss.backward()
                self.policy.actor_optimizer.step()
                self.policy.critic_optimizer.zero_grad()
                value_loss = (val - ret).pow(2).mean()
                value_loss.backward()
                self.policy.critic_optimizer.step()

    def __parse_model_name_feats(self, model_name):
        feats = model_name.split("_")
        alg = feats[0]
        epoch = int(feats[8])
        elapse = float(feats[10]) / 60.0
        cmt = "_".join(feats[12:])
        return {"alg": alg, "epoch": epoch, "elapse": elapse, "cmt": cmt}

