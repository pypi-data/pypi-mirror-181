import os, sys

sys.path.append(os.path.dirname(__file__))

from copy import deepcopy
from typing import Any, Dict, Optional, Union

from tianshou.data import Batch, ReplayBuffer, to_numpy, to_torch_as
from tianshou.policy import DQNPolicy

import torch
from tianshou.utils.net.common import MLP
import torch.nn as nn
import numpy as np
from torch.nn.functional import softplus
from torch.distributions import Normal, Independent
import torch.nn.functional as F
import math
import random
from itertools import combinations
from other import make_path_if_not_exist
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import seaborn as sns


def update_beta(method, beta, loss_infomin=None, acc=None, min_val=None, set_beta=None):
    def add_beta(beta):
        return min(beta + step_val, max_val)

    def reduce_beta(beta):
        return max(beta - step_val, min_val)


    if set_beta is not None:
        return set_beta

    max_val = 1
    min_val = 0.001 if min_val is None else min_val
    step_val = 1e-3

    if method == 'InfoGoal':
        return add_beta(beta) if acc > 0.95 else reduce_beta(beta)
    elif method == 'InfoBot':
        return 0.01
    else:
        return beta


def reparameterization(params, z_dim, num_sample=1):
    mu, sigma = params[:, :z_dim], params[:, z_dim:]
    sigma = softplus(sigma) + 1e-3  # Make sigma always positive
    if num_sample == 1:
        z = Independent(Normal(loc=mu, scale=sigma), 1).rsample()
    else:
        z = Independent(Normal(loc=mu, scale=sigma), 1).rsample(sample_shape=(num_sample,))
    return z, mu, sigma

def infomax_loss_fn_two_goal_repre(z0,z1):
    return  F.l1_loss(z0, z1, reduction='none')

def infomax_loss_fn(z_p0, z_p1, z_n0, z_n1, method='our', W=None):
    if method == 'our':
        z_pos = infomax_loss_fn_two_goal_repre(z_p0,z_p1)
        z_neg = infomax_loss_fn_two_goal_repre(z_n0,z_n1)

        z_pos = torch.mean(z_pos, dim=-1)
        z_neg = torch.mean(z_neg, dim=-1)
        loss = torch.exp(z_pos - z_neg)
        loss = torch.mean(loss)

        acc = torch.mean(torch.as_tensor(z_pos < z_neg, dtype=torch.float32))
        return loss, acc
    elif method == 'wmse':
        num_goal = int(len(z_p0))
        z = torch.cat([z_p0, z_p1], dim=0)
        z = W(z)
        z_a = z[:num_goal]
        z_p = z[num_goal:]
        loss = (z_a - z_p).pow(2).mean()
        return loss, torch.FloatTensor([0.])


def infomin_loss_fn(mu, std, reduction='mean'):
    # loss = F.mse_loss(std, torch.ones_like(std))+F.mse_loss(mu, torch.zeros_like(mu))
    if reduction == 'mean':
        loss = -0.5 * (1 + 2 * std.log() - mu.pow(2) - std.pow(2)).sum(1).mean().div(math.log(2))
    elif reduction == 'none':
        loss = -0.5 * (1 + 2 * std.log() - mu.pow(2) - std.pow(2)).sum(1).div(math.log(2))
    return loss


def draw_scatter_emb(net, save_path, env_info, env, times, device, show_goal_id_set=None, enlarge_goal_id=None):
    make_path_if_not_exist(os.path.dirname(save_path))

    SMALL_SIZE = 6 * times
    MEDIUM_SIZE = 8 * times

    plt.rc('pdf', fonttype=42)
    plt.rc('ps', fonttype=42)
    plt.rc('font', family='serif')
    plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title

    goal_info_dict = env_info['goal_info_dict']
    c_dict = env_info['c_dict']

    cur_goal_ids = []
    cur_goals = []
    cur_colors = []
    cur_modes = []
    cur_sizes = []
    for cur_goal_id in goal_info_dict.keys():
        if show_goal_id_set is not None:
            if cur_goal_id not in show_goal_id_set:
                continue
        cur_mode = 'training' if cur_goal_id in env.training_goal_ids else 'test'
        if (enlarge_goal_id is not None) and (cur_mode == 1) and (cur_goal_id != enlarge_goal_id): continue
        cur_modes.append(cur_mode)
        cur_goal_ids.append(cur_goal_id)
        cur_colors.append(goal_info_dict[cur_goal_id]['room'])
        if cur_goal_id == enlarge_goal_id:
            cur_sizes.append(400)
        else:
            cur_sizes.append(200)

    with torch.no_grad():
        z, m, s = net.encode_fn(cur_goal_ids, type='goal', num_sample=100)
        z_orig_shape = z.shape
        if len(z_orig_shape) == 2:
            z_orig_shape = (1, *z_orig_shape)
        num_repeat = z_orig_shape[0]
        num_goal = z_orig_shape[1]
        num_dim = z_orig_shape[2]

        cur_colors_for_z = cur_colors*num_repeat #[cur_color for cur_color in cur_colors for i in range(num_repeat)]
        cur_modes_for_z = cur_modes*num_repeat #[cur_mode for cur_mode in cur_modes for i in range(num_repeat)]
        cur_sizes_for_z = cur_sizes*num_repeat #[cur_size for cur_size in cur_sizes for i in range(num_repeat)]

        cur_colors_for_m = cur_colors
        cur_modes_for_m = cur_modes
        cur_sizes_for_m = cur_sizes

        # cur_colors_for_z = np.asarray(cur_colors)[None, ...].repeat(z_orig_shape[0], axis=0).reshape(-1, 1)
        # cur_modes_for_z = np.asarray(cur_modes)[None, ...].repeat(z_orig_shape[0], axis=0).reshape(-1, 1)
        # cur_sizes_for_z = np.asarray(cur_sizes)[None, ...].repeat(z_orig_shape[0], axis=0).reshape(-1, 1)

        # cur_colors_for_m = np.asarray(cur_colors).reshape(-1, 1)
        # cur_modes_for_m = np.asarray(cur_modes).reshape(-1, 1)
        # cur_sizes_for_m = np.asarray(cur_sizes).reshape(-1,1)

        z = z.reshape(-1, num_dim).cpu().numpy()
        z_2d = z if num_dim == 2 else PCA(n_components=2).fit_transform(z)
        m_2d = np.mean(z_2d.reshape(z_orig_shape[0], z_orig_shape[1], -1), axis=0)

        z_2d_w_color = [[z2i[0], z2i[1], cur_color_for_z, cur_mode_for_z, cur_size_for_z] for
                        z2i, cur_color_for_z, cur_mode_for_z, cur_size_for_z in
                        zip(z_2d, cur_colors_for_z, cur_modes_for_z, cur_sizes_for_z)]
        m_2d_w_color = [[m2i[0], m2i[1], cur_color_for_m, cur_mode_for_m, cur_size_for_m] for
                        m2i, cur_color_for_m, cur_mode_for_m, cur_size_for_m in
                        zip(m_2d, cur_colors_for_m, cur_modes_for_m, cur_sizes_for_m)]


        # z_2d_w_color = np.concatenate([z_2d, cur_colors_for_z, cur_modes_for_z, cur_sizes_for_z], axis=-1)
        # m_2d_w_color = np.concatenate([m_2d, cur_colors_for_m, cur_modes_for_m, cur_sizes_for_m], axis=-1)

    z_pd = pd.DataFrame(z_2d_w_color, columns=['x', 'y', 'room', 'mode', 'size'])
    m_pd = pd.DataFrame(m_2d_w_color, columns=['x', 'y', 'room', 'mode', 'size'])

    # m_pd = m_pd.replace({'mode': {0: 'training', 1: 'test'}})
    # m_pd = m_pd.replace({'room': {0: 'A', 1: 'B', 2: 'C', 3: 'D'}})

    ax = plt.gca()
    sns.scatterplot(ax=ax, data=z_pd, x='x', y='y',
                    alpha=0.1, style='mode', markers={'training': 'o', 'test': '*'}, s=400,
                    hue='room', palette=c_dict, legend=False)
    sns.scatterplot(ax=ax, data=m_pd, x='x', y='y',
                    style='mode', markers={'training': 'o', 'test': '*'}, s=400,
                    hue='room', palette=c_dict, legend=True)

    # for label, (marker, s) in {'training goal': ('o', 200), 'test goal': ('*', 400)}.items():
    #     plt.scatter([], [], s=s, marker=marker, label=label, facecolors='none', edgecolors='k')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), shadow=True, markerscale=2)  # ,

    # ax.axis('off')
    # ax.set_aspect('auto')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

class Base:

    def __init__(self, net, optim, batch_size, positive_instance_pairs):
        self.net = net
        self.optim = optim
        self.device = net.device
        self.batch_size = batch_size
        self.positive_instance_pairs = positive_instance_pairs
        self.len_positive_instance_pairs = None
        self.pos_pair_set = None
        self.neg_pair_set = None

    def divide_pos_neg_pairs(self, ):
        if (self.len_positive_instance_pairs is not None) and \
                (len(self.positive_instance_pairs) == self.len_positive_instance_pairs):
            return

        self.len_positive_instance_pairs = len(self.positive_instance_pairs)

        # get z_a
        a = []
        for pair in self.positive_instance_pairs:
            a += list(pair)
        a = set(a)

        pos_pair_set = []
        for ai in a:
            pos = []
            for pair in self.positive_instance_pairs:
                if ai in pair:
                    pos += list(pair)
            pos = set(pos)

            for posi in pos:
                pos_pair_set.append([ai, posi])

        neg_pair_set = []
        for pair in combinations(a, 2):
            is_pos = False
            for pos_pair in pos_pair_set:
                if ((pair[0] == pos_pair[0]) and (pair[1] == pos_pair[1])) or (pair[1] == pos_pair[0]) and (
                        pair[0] == pos_pair[1]):
                    is_pos = True
                    break

            if not is_pos:
                neg_pair_set.append(pair)

        self.pos_pair_set = pos_pair_set
        self.neg_pair_set = neg_pair_set

    def forward(self):
        raise NotImplementedError

    def update(self):
        self.optim.zero_grad()
        loss, loss_breakdown = self.forward()
        loss.backward()
        self.optim.step()

        desc = " ".join(['{} {:.3f}'.format(k, v) for k, v in loss_breakdown.items()])
        return desc


class InfoMax(Base):

    def __init__(self, net, optim, batch_size, positive_instance_pairs):
        super().__init__(
            net=net, optim=optim, batch_size=batch_size,
            positive_instance_pairs=positive_instance_pairs
        )

    def forward(self):
        self.divide_pos_neg_pairs()
        if (self.pos_pair_set is None) or \
                ((self.neg_pair_set is None)) or \
                (min(len(self.neg_pair_set), len(self.pos_pair_set)) == 0):
            return {'loss': None}

        num_sample = min(len(self.neg_pair_set), len(self.pos_pair_set))
        pos_pairs = np.asarray(random.sample(self.pos_pair_set, num_sample))
        neg_pairs = np.asarray(random.sample(self.neg_pair_set, num_sample))

        a = torch.as_tensor(self.net.goal_set[pos_pairs[:, 0]], dtype=torch.float32, device=self.net.device)
        b = torch.as_tensor(self.net.goal_set[pos_pairs[:, 1]], dtype=torch.float32, device=self.net.device)
        c = torch.as_tensor(self.net.goal_set[neg_pairs[:, 0]], dtype=torch.float32, device=self.net.device)
        d = torch.as_tensor(self.net.goal_set[neg_pairs[:, 1]], dtype=torch.float32, device=self.net.device)

        abcd = torch.cat([a, b, c, d])
        z_abcd, mu, std = self.net.encode_goal(abcd)
        z_a, z_b, z_c, z_d = torch.chunk(z_abcd, 4)

        loss_infomax, infomax_acc = infomax_loss_fn(z_p0=z_a, z_p1=z_b, z_n0=z_c, z_n1=z_d)

        return {'loss': loss_infomax, 'acc': infomax_acc,
                'mu': mu, 'std': std}


class InfoMin(Base):

    def __init__(self, net, optim, batch_size, positive_instance_pairs):
        super().__init__(
            net=net, optim=optim, batch_size=batch_size,
            positive_instance_pairs=positive_instance_pairs
        )

    def forward(self, mu=None, std=None):

        if mu is None:
            pair = np.asarray(list(self.positive_instance_pairs)).copy()
            np.random.shuffle(pair)
            anc = pair[:self.batch_size, 0]
            pos = pair[:self.batch_size, 1]

            if random.random() < 0.5:
                tmp = anc.copy()
                anc = pos.copy()
                pos = tmp

            anc = torch.as_tensor(self.net.goal_set[anc], dtype=torch.float32,
                                  device=self.net.device)
            pos = torch.as_tensor(self.net.goal_set[pos], dtype=torch.float32,
                                  device=self.net.device)

            z_a, m_a, s_a = self.net.encode_goal(anc)
            with torch.no_grad():
                z_pos, m_p, s_p = self.net.encode_goal(pos)

            mu = torch.cat([m_a, m_p])
            std = torch.cat([s_a, s_p])

        loss = infomin_loss_fn(mu, std)
        return {'loss': loss}
