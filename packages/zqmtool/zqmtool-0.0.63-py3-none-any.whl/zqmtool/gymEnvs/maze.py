import gym
import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque
from itertools import combinations
from collections import defaultdict
import cv2
import copy
import os
from zqmtool.other import remove_make_path, get_row_index_in_arr, get_rgba_from_cmap

random.seed(0)
np.random.seed(0)

wall = np.array([
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
], dtype=int)

init_pos = [5,5]

train_goal_states = np.asarray([
    [0, 0], [3, 0], [0, 3], [3, 3],
    [0, 7], [0, 10], [3, 7], [3, 10],
    [10, 0], [10, 3], [7, 0], [7, 3],
    [7, 10], [10, 10], [7, 7], [10, 7]
])

room_bound = {0: np.asarray([[0, 3], [0, 3]]),
              1: np.asarray([[0, 3], [7, 10]]),
              2: np.asarray([[7, 10], [0, 3]]),
              3: np.asarray([[7, 10], [7, 10]])}

# wall = np.array([
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
# ], dtype=int)
# # plt.imshow(wall)
# # plt.show()
#
#
# train_goal_states = np.asarray([
#     [0, 0], [4, 0], [0, 4], [4, 4],
#     [0, 8], [0, 12], [4, 8], [4, 12],
#     [12, 0], [12, 4], [8, 0], [8, 4],
#     [8, 12], [12, 12], [8, 8], [12, 8]
# ])
#
# room_bound = {0: np.asarray([[0, 4], [0, 4]]),
#               1: np.asarray([[0, 4], [8, 12]]),
#               2: np.asarray([[8, 12], [0, 4]]),
#               3: np.asarray([[8, 12], [8, 12]])}


def gen_uninformative_goal_from_goal_state(goal_state, goal_id, num_goal):
    # # wh = max(wall.shape)
    # wh = 10
    # rnd = wh * np.random.random(size=(wh,))
    # # rnd_id = random.choice(range(0,9))
    # rnd_id = int(wh / 2)
    # rnd[rnd_id:rnd_id + 2] = goal_state.copy()
    # goal = rnd.copy()

    import torch
    import torch.nn as nn
    torch.manual_seed(0)

    encoder = nn.Embedding(num_embeddings=num_goal, embedding_dim=10)
    with torch.no_grad():
        goal = encoder(torch.LongTensor([goal_id]))[0].numpy().tolist()
    return goal


def get_goal_dataset(wall):
    goal_info_dict = {}
    goal_state_to_goal_id = defaultdict(dict)
    goal_id = -1
    goal_set = []

    state_set = np.stack(np.where(wall == 0), axis=-1)

    for state_id, state in enumerate(state_set):
        goal_state = state.copy()

        cur_room_id = None
        for room_id, bounds in room_bound.items():
            x_bound, y_bound = bounds
            if (goal_state[0] in range(x_bound[0], x_bound[1] + 1)) and (
                    goal_state[1] in range(y_bound[0], y_bound[1] + 1)):
                cur_room_id = room_id
                break
        if cur_room_id is None:
            continue

        goal_id += 1

        goal = gen_uninformative_goal_from_goal_state(goal_state, goal_id, num_goal=len(state_set))

        goal_set.append(goal)

        mode = 'train' if get_row_index_in_arr(goal_state, train_goal_states) is not False else 'test'

        goal_state_to_goal_id[goal_state[0]][goal_state[1]] = goal_id

        goal_info_dict[goal_id] = {'goal': goal, 'mode': mode, 'goal_state': goal_state, 'room_id': cur_room_id}

    goal_set = np.asarray(goal_set)

    return goal_set, state_set, goal_info_dict, goal_state_to_goal_id


goal_set, state_set, goal_info_dict, goal_state_to_goal_id = get_goal_dataset(wall)

positive_goal_id_pair = set()


class Env(gym.Env):

    def __init__(self, mode, random_initial_state, can_see_test_goal=True):
        super().__init__()
        self.can_see_test_goal = can_see_test_goal
        self.mode = mode
        self.height, self.width = wall.shape

        self.actions = [
            np.array([0, 1]),  # Up
            np.array([1, 0]),  # Right
            np.array([0, -1]),  # Down
            np.array([-1, 0]),  # Left,
        ]

        self.goal_dataset = {goal_id: goal_info for goal_id, goal_info in goal_info_dict.items() if
                             goal_info['mode'] == self.mode}

        self.state_dim = state_set.shape[-1]
        self.goal_dim = len(list(self.goal_dataset.values())[0]['goal'])

        self.random_initial_state = random_initial_state if random_initial_state is not None else \
            {'train': True, 'test': False}[mode]

        self.T = 100  # if random_initial_state == True else 500

        self.action_space = gym.spaces.Discrete(n=len(self.actions))
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(2 + self.goal_dim,))

    def vis_goal_state_pair(self, ):
        logdir = 'vis_gpal_state_pair'
        remove_make_path(logdir)
        for pair in positive_goal_id_pair:
            g_id_0, g_id_1 = pair

            if not os.path.exists(f'{g_id_0} {g_id_1}.png'):
                g_s_0 = self.goal_dataset[g_id_0]['goal_state']
                g_s_1 = self.goal_dataset[g_id_1]['goal_state']
                wall_copy = wall.copy()
                wall_copy[g_s_0[0], g_s_0[1]] = 2
                wall_copy[g_s_1[0], g_s_1[1]] = 2
                plt.imshow(wall_copy)
                plt.savefig(os.path.join(logdir, f'{g_id_0} {g_id_1}.png'))
                plt.close()

    def check_success(self, ):
        return (self.pos[0] == self.goal_state[0]) and (self.pos[1] == self.goal_state[1])

    def update_state(self, a):

        def f():
            if (self.pos[0] in goal_state_to_goal_id.keys()) and \
                    (self.pos[1] in goal_state_to_goal_id[self.pos[0]].keys()):
                self.achieved_goal_id = goal_state_to_goal_id[self.pos[0]][self.pos[1]]
                if (not self.can_see_test_goal) and (goal_info_dict[self.achieved_goal_id]['mode'] == 'test'):
                    self.achieved_goal_id = -1
            else:
                self.achieved_goal_id = -1
            self.time_window.append(self.achieved_goal_id)
            self.update_positive_goal_id_pair()

        if a is not None:
            a = self.actions[a]
            tmp_pos = self.pos.copy() + a
            x, y = tmp_pos
            if (x >= 0 and x < self.height) and (y >= 0 and y < self.width) and (wall[x, y] == 0):
                self.pos = tmp_pos
                self.pos_id = get_row_index_in_arr(self.pos, state_set)

        f()

        self.cur_goal_id = -1
        if (self.achieved_goal_id >= 0) and (self.achieved_goal_id not in self.achieved_goal_id_set):
            self.cur_goal_id = copy.deepcopy(self.achieved_goal_id)
            self.achieved_goal_id_set.add(self.achieved_goal_id)

    def update_positive_goal_id_pair(self, ):
        time_window_no_neg = [elem for elem in set(self.time_window) if elem >= 0]
        adjecent_goal_id_pairs = set(combinations(time_window_no_neg, 2))
        positive_goal_id_pair.update(adjecent_goal_id_pairs)

    def get_mask(self):
        mask = []
        for act in self.actions:
            tmp_pos = self.pos.copy() + act
            x, y = tmp_pos
            if (x >= 0 and x < self.height) and (y >= 0 and y < self.width) and (wall[x, y] == 0):
                mask.append(True)
            else:
                mask.append(False)
        return mask

    def get_obs(self):
        return {'state_id': self.pos_id, 'cur_goal_id': self.cur_goal_id + 1, 'goal_id': self.goal_id,
                'hindsight_goal_id': self.achieved_goal_id,
                'mask': self.get_mask(),
                'max_rew': 10., 'mode': self.mode}

    def reset(self, **kwargs):
        self.t = 0

        self.achieved_goal_id = None
        self.achieved_goal_id_set = set()

        self.time_window = deque(maxlen=10)

        self.goal_id = random.choice(list(self.goal_dataset.keys()))
        self.goal_state, self.goal = self.goal_dataset[self.goal_id]['goal_state'], \
                                     self.goal_dataset[self.goal_id]['goal']

        self.pos = state_set[random.choice(range(len(state_set)))] \
            if self.random_initial_state else np.asarray(init_pos)
        self.pos_id = get_row_index_in_arr(self.pos, state_set)

        self.update_state(a=None)

        return self.get_obs()

    def step(self, action):
        self.t += 1

        self.update_state(action)
        success = self.check_success()

        done = (self.t == self.T) or (success)

        rew = 10 * float(success) - 1 / self.T + float(self.cur_goal_id > 0)

        return self.get_obs(), rew, done, {}


def make_env(mode, random_initial_state=None):
    return Env(mode, random_initial_state)


env = make_env(mode='train')

output_for_goal_representation_learning = {
    'wall': wall,
    'g_dim': env.goal_dim,
    'state_dim': np.prod(env.state_dim),
    'act_dim': env.action_space.n,
    'state_set': state_set,
    'goal_set': goal_set,
    'adjacent_goal_id_pairs': positive_goal_id_pair,
    'goal_info_dict': goal_info_dict,
    'c_dict': {k: get_rgba_from_cmap('Set2', k) for k in range(4)},
}

if __name__ == '__main__':
    env = Env(mode='train', random_initial_state=True)

    for i in range(1):

        s = env.reset()
        d = False
        wall_copy = wall.copy()
        while not d:
            pos = state_set[env.pos_id]
            wall_copy[pos[0], pos[1]] = 2
            s, r, d, _ = env.step(env.action_space.sample())
