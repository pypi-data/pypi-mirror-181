from copy import deepcopy
from typing import Any, Dict, Optional, Union

from tianshou.data import Batch, to_torch_as
from tianshou.policy import DQNPolicy

import torch
from tianshou.utils.net.common import MLP
import torch.nn as nn
import numpy as np


class Policy(DQNPolicy):
    """Implementation of Deep Q Network. arXiv:1312.5602.

    Implementation of Double Q-Learning. arXiv:1509.06461.

    Implementation of Dueling DQN. arXiv:1511.06581 (the dueling DQN is
    implemented in the network side, not here).

    :param torch.nn.Module model: a model following the rules in
        :class:`~tianshou.policy.BasePolicy`. (s -> logits)
    :param torch.optim.Optimizer optim: a torch.optim for optimizing the model.
    :param float discount_factor: in [0, 1].
    :param int estimation_step: the number of steps to look ahead. Default to 1.
    :param int target_update_freq: the target network update frequency (0 if
        you do not use the target network). Default to 0.
    :param bool reward_normalization: normalize the reward to Normal(0, 1).
        Default to False.
    :param bool is_double: use double dqn. Default to True.

    .. seealso::

        Please refer to :class:`~tianshou.policy.BasePolicy` for more detailed
        explanation.
    """

    def __init__(
            self,
            goal_representation_learner,
            state_representation_learner,
            model: torch.nn.Module,
            optim: torch.optim.Optimizer,
            discount_factor: float = 0.99,
            estimation_step: int = 1,
            target_update_freq: int = 0,
            reward_normalization: bool = False,
            is_double: bool = True,
            **kwargs: Any,
    ) -> None:
        super().__init__(model, optim, discount_factor, estimation_step,
                         target_update_freq, reward_normalization, is_double, **kwargs)
        self.goal_representation_learner = goal_representation_learner
        self.state_representation_learner = state_representation_learner

    def learn(self, batch: Batch, **kwargs: Any) -> Dict[str, float]:
        loss_breakdown = {}
        if self._target and self._iter % self._freq == 0:
            self.sync_weight()
        self.optim.zero_grad()
        weight = batch.pop("weight", 1.0)
        q = self(batch).logits
        q = q[np.arange(len(q)), batch.act]
        r = to_torch_as(batch.returns.flatten(), q)
        td = r - q
        loss = (td.pow(2) * weight).mean()
        batch.weight = td  # prio-buffer

        loss_breakdown.update({'rl': loss.item()})

        loss_g, loss_g_breakdown = self.goal_representation_learner.forward(batch=batch)
        loss_s, loss_s_breakdown = self.state_representation_learner.forward(batch=batch)

        if loss_g is not None:
            loss_breakdown.update(loss_g_breakdown)
            loss = loss + loss_g

        if loss_s is not None:
            loss_breakdown.update(loss_s_breakdown)
            loss = loss + loss_s

        loss.backward()

        self.optim.step()

        self._iter += 1

        return loss_breakdown
