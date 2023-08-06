import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
from torch.distributions.normal import Normal

from rlvortex.utils.trainer_utils import v_debug


class BaseActor(nn.Module):
    def __init__(self, *, net: nn.Module):
        super().__init__()
        self.logits_net = net

    def _distribution(self, obs):
        raise NotImplementedError

    def _log_prob_from_distribution(self, pi, act):
        raise NotImplementedError


class BaseCritic(nn.Module):
    def __init__(self, *, net: nn.Module):
        super().__init__()
        self.v_net = net

    def forward(self, obs):
        return torch.squeeze(self.v_net(obs), -1)  # squeeze values from (obs_dim, 1) to (obs_dim,)


class CategoricalActor(BaseActor):
    def __init__(self, *, net: nn.Module):
        super().__init__(net=net)

    def _distribution(self, obs):
        logits = self.logits_net(obs)
        return Categorical(logits=logits)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act)  # flat actions to 1-dim tensor for Categorical distribution


class GaussianActor(BaseActor):
    def __init__(self, *, net: nn.Module, init_log_std: torch.Tensor):
        super().__init__(net=net)
        self.log_std = init_log_std

    def _distribution(self, obs):
        mu = self.logits_net(obs)
        std = torch.exp(self.log_std)
        return Normal(mu, std)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act).sum(axis=-1)  # Last axis sum needed for Torch Normal distribution

    def to(self, device):
        self.mu_net = self.mu_net.to(device)
        self.log_std = self.log_std.to(device)
        return self


class BasePPOPolicy(nn.Module):
    def __init__(
        self, actor: BaseActor, critic: BaseCritic, optimizer: torch.optim.Optimizer, learning_rate: float = 3e-4
    ) -> None:
        super().__init__()

        self.actor: BaseActor = actor
        self.critic: BaseCritic = critic
        self._learning_rate: float = learning_rate
        self.optimizer = optimizer(self.parameters(), lr=self._learning_rate)
        self.actor_optimizer = optimizer(self.actor.parameters(), lr=3e-4)
        self.critic_optimizer = optimizer(self.critic.parameters(), lr=1e-3)

    @property
    def learning_rate(self):
        return self._learning_rate

    def update_learning_rate(self, learning_rate):
        self._learning_rate = learning_rate
        for param_group in self.optimizer.param_groups:
            param_group["lr"] = self._learning_rate

    def _distribution(self, obs):
        return self.actor.distribution(obs)

    def _log_prob_from_distribution(self, pi, act):
        return self.actor.log_prob_from_distribution(pi, act)

    """
    This method is used to interact with the environment. No gradient is computed.
    """

    def act(self, observation):
        with torch.no_grad():
            pi = self.actor._distribution(observation)
            a = pi.sample()
            logp_a = self.actor._log_prob_from_distribution(pi, a)
            v = self.critic(observation)
            return a, logp_a, v

    """
    This method is used to compute the loss. Graident is computed.
    """

    def forward(self, actions, observations):
        pi = self.actor._distribution(observations)
        logp_a = self.actor._log_prob_from_distribution(pi, actions)
        v = self.critic(observations)
        entropy = pi.entropy().mean()
        return logp_a, v, entropy

    def to(self, device):
        self.actor = self.actor.to(device)
        self.critic = self.critic.to(device)
        return self

    def step(self, obs):
        with torch.no_grad():
            pi = self.actor._distribution(obs)
            a = pi.sample()
            logp_a = self.actor._log_prob_from_distribution(pi, a)
            v = self.critic(obs)
        return a, v, logp_a

    def act(self, obs):
        return self.step(obs)[0]

    def actor_forward(self, obs, act=None):
        pi = self.actor._distribution(obs)
        logp_a = None
        if act is not None:
            logp_a = self.actor._log_prob_from_distribution(pi, act)
        return pi, logp_a
