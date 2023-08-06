import copy
import random
import time
import warnings
from typing import Any, Callable, Dict, List, Optional, Union

import gym
import numpy as np
import torch

from tianshou.data import (
    Batch,
    CachedReplayBuffer,
    ReplayBuffer,
    ReplayBufferManager,
    VectorReplayBuffer,
    to_numpy,
    Collector
)
from tianshou.data.batch import _alloc_by_keys_diff
from tianshou.env import BaseVectorEnv, DummyVectorEnv
from tianshou.policy import BasePolicy

T = 100



def get_new_trajactory_len(buffers, env_id, ep_len, relabelling_strategy, goal_info_dict):
    env_buffer = buffers[env_id]
    env_buffer_len = env_buffer.last_index[0] + 1
    traj_len = ep_len[env_id]
    obs_index_range = np.arange(env_buffer_len - traj_len, env_buffer_len) % len(env_buffer)
    original_trajectory = env_buffer[obs_index_range]

    achieved_goal_id = original_trajectory.obs_next.achieved_goal_id
    desired_goal_id = original_trajectory.obs_next.desired_goal_id
    #print(desired_goal_id)
    assert len(desired_goal_id) > 0
    assert len(np.unique(desired_goal_id)) == 1
    unique_desired_goal_id = np.unique(desired_goal_id)[0]
    achieved_goal_id = np.unique(achieved_goal_id[achieved_goal_id >= 0])

    max_rew = original_trajectory.obs_next.max_rew[0]

    if len(achieved_goal_id) == 0:
        return None, None
    # if relabelling_strategy == 'advantage':
    #     s0_id = original_trajectory.obs.state_id[0]
    #     achieved_goal_id_his = original_trajectory.obs.achieved_goal_id_his[0]
    #     s0_id = [s0_id] * len(achieved_goal_id)
    #     achieved_goal_id_his = [achieved_goal_id_his] * len(achieved_goal_id)
    #     obs = Batch({'state_id': s0_id, 'desired_goal_id': achieved_goal_id, 'achieved_goal_id_his': achieved_goal_id_his})
    #     with torch.no_grad():
    #         q, _ = q_net(obs, state=None, info=None)
    #         q = torch.amax(q, dim=-1).cpu().numpy()

    new_trajactory_len = []
    for index, achieved_goal_id_i in enumerate(achieved_goal_id):

        length_candidate = np.where(original_trajectory.obs_next.achieved_goal_id == achieved_goal_id_i)[0]
        if relabelling_strategy == 'min_length':
            length = np.amin(length_candidate)
        elif relabelling_strategy == 'cher':
            if goal_info_dict[unique_desired_goal_id]['room'] != goal_info_dict[achieved_goal_id_i]['room']:
                continue
            length = np.amin(length_candidate)
        elif relabelling_strategy == 'random':
            length = random.choice(length_candidate)
        # elif relabelling_strategy == 'advantage':
        #     length = np.amin(length_candidate)
        #     q_i = q[index]
        #     cumulative_reward = -(length - 1) * (1 / T) + max_rew
        #     if q_i > cumulative_reward:
        #         continue
        else:
            raise NotImplementedError
        new_trajactory_len.append(length)

    if len(new_trajactory_len) == 0:
        return None, None

    return new_trajactory_len, original_trajectory


class HERCollector(Collector):
    def __init__(self,
                 policy: BasePolicy,
                 env: Union[gym.Env, BaseVectorEnv],
                 buffer: Optional[ReplayBuffer] = None,
                 preprocess_fn: Optional[Callable[..., Batch]] = None,
                 exploration_noise: bool = False,
                 max_len: int = 1e6,
                 ):
        super(HERCollector, self).__init__(
            policy,
            env,
            buffer,
            preprocess_fn,
            exploration_noise
        )
        self.max_len = max_len
        self.relabelling_strategy = 'random'
        self.goal_info_dict =  env.workers[0].env.goal_info_dict

    def collect(
            self,
            n_step: Optional[int] = None,
            n_episode: Optional[int] = None,
            random: bool = False,
            render: Optional[float] = None,
            no_grad: bool = True,
    ) -> Dict[str, Any]:
        """Collect a specified number of step or episode.

        To ensure unbiased sampling result with n_episode option, this function will
        first collect ``n_episode - env_num`` episodes, then for the last ``env_num``
        episodes, they will be collected evenly from each env.

        :param int n_step: how many steps you want to collect.
        :param int n_episode: how many episodes you want to collect.
        :param bool random: whether to use random policy for collecting data. Default
            to False.
        :param float render: the sleep time between rendering consecutive frames.
            Default to None (no rendering).
        :param bool no_grad: whether to retain gradient in policy.forward(). Default to
            True (no gradient retaining).

        .. note::

            One and only one collection number specification is permitted, either
            ``n_step`` or ``n_episode``.

        :return: A dict including the following keys

            * ``n/ep`` collected number of episodes.
            * ``n/st`` collected number of steps.
            * ``rews`` array of episode reward over collected episodes.
            * ``lens`` array of episode length over collected episodes.
            * ``idxs`` array of episode start index in buffer over collected episodes.
            * ``rew`` mean of episodic rewards.
            * ``len`` mean of episodic lengths.
            * ``rew_std`` standard error of episodic rewards.
            * ``len_std`` standard error of episodic lengths.
        """
        assert not self.env.is_async, "Please use AsyncCollector if using async venv."
        if n_step is not None:
            assert n_episode is None, (
                f"Only one of n_step or n_episode is allowed in Collector."
                f"collect, got n_step={n_step}, n_episode={n_episode}."
            )
            assert n_step > 0
            if not n_step % self.env_num == 0:
                warnings.warn(
                    f"n_step={n_step} is not a multiple of #env ({self.env_num}), "
                    "which may cause extra transitions collected into the buffer."
                )
            ready_env_ids = np.arange(self.env_num)
        elif n_episode is not None:
            assert n_episode > 0
            ready_env_ids = np.arange(min(self.env_num, n_episode))
            self.data = self.data[:min(self.env_num, n_episode)]
        else:
            raise TypeError(
                "Please specify at least one (either n_step or n_episode) "
                "in AsyncCollector.collect()."
            )

        start_time = time.time()

        step_count = 0
        episode_count = 0
        episode_rews = []
        episode_lens = []
        episode_start_indices = []

        while True:
            assert len(self.data) == len(ready_env_ids)
            # restore the state: if the last state is None, it won't store
            last_state = self.data.policy.pop("hidden_state", None)

            # get the next action
            if random:
                self.data.update(
                    act=[self._action_space[i].sample() for i in ready_env_ids]
                )
            else:
                if no_grad:
                    with torch.no_grad():  # faster than retain_grad version
                        # self.data.obs will be used by agent to get result
                        result = self.policy(self.data, last_state)
                else:
                    result = self.policy(self.data, last_state)
                # update state / act / policy into self.data
                policy = result.get("policy", Batch())
                assert isinstance(policy, Batch)
                state = result.get("state", None)
                if state is not None:
                    policy.hidden_state = state  # save state into buffer
                act = to_numpy(result.act)
                if self.exploration_noise:
                    act = self.policy.exploration_noise(act, self.data)
                self.data.update(policy=policy, act=act)

            # get bounded and remapped actions first (not saved into buffer)
            action_remap = self.policy.map_action(self.data.act)
            # step in env
            result = self.env.step(action_remap, ready_env_ids)  # type: ignore
            obs_next, rew, done, info = result

            self.data.update(obs_next=obs_next, rew=rew, done=done, info=info)
            if self.preprocess_fn:
                self.data.update(
                    self.preprocess_fn(
                        obs_next=self.data.obs_next,
                        rew=self.data.rew,
                        done=self.data.done,
                        info=self.data.info,
                        policy=self.data.policy,
                        env_id=ready_env_ids,
                    )
                )

            if render:
                self.env.render()
                if render > 0 and not np.isclose(render, 0):
                    time.sleep(render)

            # add data into the buffer
            ptr, ep_rew, ep_len, ep_idx = self.buffer.add(
                self.data, buffer_ids=ready_env_ids
            )

            # collect statistics
            step_count += len(ready_env_ids)

            if np.any(done):
                env_ind_local = np.where(done)[0]
                env_ind_global = ready_env_ids[env_ind_local]
                episode_count += len(env_ind_local)
                episode_lens.append(ep_len[env_ind_local])
                episode_rews.append(ep_rew[env_ind_local])
                episode_start_indices.append(ep_idx[env_ind_local])
                # now we copy obs_next to obs, but since there might be
                # finished episodes, we have to reset finished envs first.
                obs_reset = self.env.reset(env_ind_global)
                if self.preprocess_fn:
                    obs_reset = self.preprocess_fn(
                        obs=obs_reset, env_id=env_ind_global
                    ).get("obs", obs_reset)
                self.data.obs_next[env_ind_local] = obs_reset
                for i in env_ind_local:
                    self._reset_state(i)

                # remove surplus env id from ready_env_ids
                # to avoid bias in selecting environments
                if n_episode:
                    surplus_env_num = len(ready_env_ids) - (n_episode - episode_count)
                    if surplus_env_num > 0:
                        mask = np.ones_like(ready_env_ids, dtype=bool)
                        mask[env_ind_local[:surplus_env_num]] = False
                        ready_env_ids = ready_env_ids[mask]
                        self.data = self.data[mask]

                # use HER to create more trajectory
                for env_id in env_ind_global:  # enumerate env
                    # get recently collected data from buffer

                    new_trajactory_len, original_trajectory = get_new_trajactory_len(
                        buffers=self.buffer.buffers, env_id=env_id, ep_len=ep_len,
                        relabelling_strategy=self.relabelling_strategy,
                        goal_info_dict=self.goal_info_dict,
                    )

                    if new_trajactory_len is None:
                        continue

                    for length in new_trajactory_len:  # use different mid goal to resample
                        if length>self.max_len: continue
                        trajectory = Batch(original_trajectory[:length + 1], copy=True)

                        new_goal = trajectory.obs_next.achieved_goal_id[length]

                        new_goals = np.repeat([new_goal], length + 1, axis=0)
                        trajectory.obs.desired_goal_id = new_goals
                        trajectory.obs_next.desired_goal_id = new_goals
                        trajectory.rew[-1] = trajectory.obs_next.max_rew[0]
                        trajectory.done[-1] = True
                        for transition in trajectory:
                            self.buffer.buffers[env_id].add(transition)

                # ---------------------------------------------
            self.data.obs = self.data.obs_next

            if (n_step and step_count >= n_step) or \
                    (n_episode and episode_count >= n_episode):
                break

        # generate statistics
        self.collect_step += step_count
        self.collect_episode += episode_count
        self.collect_time += max(time.time() - start_time, 1e-9)

        if n_episode:
            self.data = Batch(
                obs={}, act={}, rew={}, done={}, obs_next={}, info={}, policy={}
            )
            self.reset_env()

        if episode_count > 0:
            rews, lens, idxs = list(
                map(
                    np.concatenate,
                    [episode_rews, episode_lens, episode_start_indices]
                )
            )
            rew_mean, rew_std = rews.mean(), rews.std()
            len_mean, len_std = lens.mean(), lens.std()
        else:
            rews, lens, idxs = np.array([]), np.array([], int), np.array([], int)
            rew_mean = rew_std = len_mean = len_std = 0

        return {
            "n/ep": episode_count,
            "n/st": step_count,
            "rews": rews,
            "lens": lens,
            "idxs": idxs,
            "rew": rew_mean,
            "len": len_mean,
            "rew_std": rew_std,
            "len_std": len_std,
        }

class CHERCollector(HERCollector):
    def __init__(self,
                 policy: BasePolicy,
                 env: Union[gym.Env, BaseVectorEnv],
                 buffer: Optional[ReplayBuffer] = None,
                 preprocess_fn: Optional[Callable[..., Batch]] = None,
                 exploration_noise: bool = False,
                 max_len: int = 1e6,
                 ):
        super(CHERCollector, self).__init__(
            policy,
            env,
            buffer,
            preprocess_fn,
            exploration_noise
        )
        self.max_len = max_len
        self.relabelling_strategy = 'cher'

class GHRLCollector(HERCollector):
    def __init__(self,
                 policy: BasePolicy,
                 env: Union[gym.Env, BaseVectorEnv],
                 buffer: Optional[ReplayBuffer] = None,
                 preprocess_fn: Optional[Callable[..., Batch]] = None,
                 exploration_noise: bool = False,
                 max_len: int = 1e6,
                 ):
        super(GHRLCollector, self).__init__(
            policy,
            env,
            buffer,
            preprocess_fn,
            exploration_noise
        )
        self.max_len = max_len
        self.relabelling_strategy = 'min_length'
