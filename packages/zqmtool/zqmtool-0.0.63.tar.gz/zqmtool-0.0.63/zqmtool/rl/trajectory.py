import shutil

import torch
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import cv2

from collections import defaultdict
import matplotlib.patches as patches
from open3d.visualization import Visualizer
from zqmtool.image import save_image, to_rgb
import open3d as o3d
import time
from zqmtool.multi_view_stereo import merge_pcd, visualize_pcd_list
from zqmtool.other import remove_make_path


def save_traj(collector, output_for_goal_representation_learning):
    goal_id_to_goal_info = output_for_goal_representation_learning['goal_info_dict']
    wall = output_for_goal_representation_learning['wall']
    batch, _ = collector.buffer.sample(batch_size=0)
    s_ids = batch.obs_next.state_id
    g_ids = batch.obs_next.goal_id
    ds = batch.done

    traj_infos = defaultdict(dict)
    for s_id, g_id, d_i in zip(s_ids, g_ids, ds):
        s = output_for_goal_representation_learning['state_set'][s_id]
        if g_id not in traj_infos.keys():
            traj_infos[g_id]['goal_state'] = None
            traj_infos[g_id]['state_visitation'] = np.zeros_like(wall)
        traj_infos[g_id]['goal_state'] = goal_id_to_goal_info[g_id]['goal_state']
        traj_infos[g_id]['state_visitation'][s[0], s[1]] += 1

    return traj_infos


def save_traj_2(collector, output_for_goal_representation_learning):
    state_name_set = output_for_goal_representation_learning['state_name_set']
    state_name_achieved_goal_id = output_for_goal_representation_learning['state_name_achieved_goal_id']
    goal_id_to_goal_info = output_for_goal_representation_learning['goal_info_dict']
    batch, _ = collector.buffer.sample(batch_size=0)
    s_ids = batch.obs_next.state_id
    g_ids = batch.obs_next.goal_id
    ds = batch.done

    traj_infos = defaultdict(dict)
    tmp = []
    t = 0
    for s_id, g_id, d_i in zip(s_ids, g_ids, ds):
        if g_id in tmp: continue
        t += 1
        if g_id not in traj_infos.keys():
            traj_infos[g_id]['goal_state'] = None
            traj_infos[g_id]['visited_state_names'] = []
            traj_infos[g_id]['hit_g'] = defaultdict(list)
        traj_infos[g_id]['goal_state'] = goal_id_to_goal_info[g_id]['goal_state_names']
        traj_infos[g_id]['visited_state_names'].append(state_name_set[s_id])
        for hit_g_id in state_name_achieved_goal_id[state_name_set[s_id]]:
            traj_infos[g_id]['hit_g'][hit_g_id].append({'t': t, 'state_name': state_name_set[s_id]})

        if d_i and (g_id not in tmp):
            t = 0
            tmp.append(g_id)

    for g_id in traj_infos.keys():
        traj_infos[g_id]['visited_state_names'] = list(dict.fromkeys(traj_infos[g_id]['visited_state_names']))

    return traj_infos


def draw_traj_2(annotations_dir, orig_state_dir, mode, collector, output_for_goal_representation_learning,
                test_env, args, vis, pcdOutFolder, enlarge_goal_id=None):
    c_dict = output_for_goal_representation_learning['c_dict']
    state_set = output_for_goal_representation_learning['state_set']
    goal_id_to_goal_info = output_for_goal_representation_learning['goal_info_dict']
    state_name_pcd_indicator = output_for_goal_representation_learning['state_name_pcd_indicator']
    goalId2objId = output_for_goal_representation_learning['goalId2objId']
    room_obj_id_map = output_for_goal_representation_learning['room_obj_id_map']

    traj_info = save_traj_2(collector=collector,
                            output_for_goal_representation_learning=output_for_goal_representation_learning)
    goal_ids = {'training': test_env.training_goal_ids, 'test': test_env.test_goal_ids}[mode]

    init_pcd_list = merge_pcd([], colors=None, pcdOutFolder=pcdOutFolder)
    for cur_goal_id in goal_ids:
        print(traj_info[cur_goal_id]['hit_g'])

        # if goalId2objId[cur_goal_id] not in room_obj_id_map['kitchen']: continue

        if (enlarge_goal_id is not None) and (mode == 'test') and (cur_goal_id != enlarge_goal_id): continue

        c = c_dict[goal_id_to_goal_info[cur_goal_id]['room']]
        marker = {'training': 'o', 'test': '*'}[mode]
        img_size = 2048
        colors = []
        achieved_goal_state_names = [elem['state_name'] for list in traj_info[cur_goal_id]['hit_g'].values() for elem in
                                     list]
        for indice, state_name in enumerate(traj_info[cur_goal_id]['visited_state_names']):
            if state_name in achieved_goal_state_names:
                colors.append([0, 1, 0])
                if (indice == len(traj_info[cur_goal_id]['visited_state_names']) - 1) and (
                        cur_goal_id in traj_info[cur_goal_id]['hit_g'].keys()):
                    colors[-1] = [1, 0, 0]
            else:
                colors.append([0, 0, 1])
        pcd_list = merge_pcd(traj_info[cur_goal_id]['visited_state_names'], init_pcd_list=init_pcd_list, colors=colors,
                             pcdOutFolder=pcdOutFolder)

        state = visualize_pcd_list(pcd_list, vis, show=False)
        # state = state[169:1953, 425:2069, :]

        out_dir = os.path.join(args.logdir,
                               f"traj/{mode} {int(cur_goal_id in traj_info[cur_goal_id]['hit_g'].keys())} objID {goalId2objId[cur_goal_id]} num hit goal {len(traj_info[cur_goal_id]['hit_g'])}")
        remove_make_path(out_dir)
        save_image(os.path.join(out_dir, 'slam.png'), state)

        for hit_g_id in traj_info[cur_goal_id]['hit_g'].keys():
            for hit_goal_info in traj_info[cur_goal_id]['hit_g'][hit_g_id]:
                state_name = hit_goal_info['state_name']
                t = hit_goal_info['t']
                aux_title = 'achievedObj' if hit_g_id != cur_goal_id else 'desiredObj'
                src_orig_state_dir = os.path.join(orig_state_dir, state_name)
                dst_state_dir = os.path.join(out_dir, '{} {}'.format(aux_title, state_name))
                shutil.copy(src=src_orig_state_dir, dst=dst_state_dir)


def draw_traj(epoch, mode, collector, output_for_goal_representation_learning, test_env, args, enlarge_goal_id=None):
    def draw_training_goal_state(ax):
        for training_goal_id in [elem for elem in goal_id_to_goal_info.keys() if
                                 goal_id_to_goal_info[elem]['mode'] == 'train']:
            c = c_dict[goal_id_to_goal_info[training_goal_id]['room_id']]
            marker = {'train': 'o', 'test': '*'}['train']
            g_s = goal_id_to_goal_info[training_goal_id]['goal_state']
            ax.scatter(g_s[1] + 0.5, g_s[0] + 0.5, marker=marker, c=c, s=200)
        return ax

    c_dict = output_for_goal_representation_learning['c_dict']
    state_set = output_for_goal_representation_learning['state_set']
    goal_id_to_goal_info = output_for_goal_representation_learning['goal_info_dict']

    traj_info = save_traj(collector=collector,
                          output_for_goal_representation_learning=output_for_goal_representation_learning)

    for cur_goal_id in [elem for elem in goal_id_to_goal_info.keys() if goal_id_to_goal_info[elem]['mode'] == mode]:

        if (enlarge_goal_id is not None) and (mode == 'test') and (cur_goal_id != enlarge_goal_id): continue

        c = c_dict[goal_id_to_goal_info[cur_goal_id]['room_id']]
        marker = {'train': 'o', 'test': '*'}[mode]

        ax = plt.gca()
        ax.axis('off')
        # ax.set_aspect('auto')

        heatmap = sns.heatmap(ax=ax, data=traj_info[cur_goal_id]['state_visitation'], cmap='OrRd')
        cbar = heatmap.collections[0].colorbar
        cbar.set_ticks([])
        cbar.set_label('state visitation count for test goal')

        obs = test_env.reset()
        s_id = obs['state_id']
        init_s = state_set[s_id]
        ax.scatter(init_s[0] + 0.5, init_s[1] + 0.5, marker='s', c='b', s=200)
        for goal_id in traj_info.keys():
            if goal_id != cur_goal_id: continue
            g_s = traj_info[goal_id]['goal_state']
            ax.scatter(g_s[1] + 0.5, g_s[0] + 0.5, marker=marker, c=c, s=400)

        for block_pos in np.stack(np.where(wall == 1), axis=-1):
            ax.add_patch(
                patches.Rectangle(xy=(block_pos[1], block_pos[0]), width=1, height=1, facecolor='k', fill=True))

        ax = draw_training_goal_state(ax)

        # for label, (marker, s) in {'training goal': ('o', 200), 'test goal': ('*', 400)}.items():
        #     plt.scatter([], [], s=s, marker=marker, label=label, facecolors='none', edgecolors='k')
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), shadow=True, ncol=2)  # , markerscale=3

        plt.savefig(os.path.join(args.logdir, f'{epoch}_{mode}_{args.rl}_{args.method}_{cur_goal_id}.png'),
                    bbox_inches='tight')
        plt.close()
