import sys
sys.path.extend(['../'])

import os
import json
import pickle
import argparse

import numpy as np
from tqdm import tqdm
from torch.utils.data import Dataset
from feeders import tools

num_joint = 25
max_frame = 300
num_person_out = 1
num_person_in = 3


class Feeder_kinetics(Dataset):
    """ Feeder for skeleton-based action recognition in kinetics-skeleton dataset
    # Joint index:
    # {0,  "Nose"}
    # {1,  "Neck"},
    # {2,  "RShoulder"},
    # {3,  "RElbow"},
    # {4,  "RWrist"},
    # {5,  "LShoulder"},
    # {6,  "LElbow"},
    # {7,  "LWrist"},
    # {8,  "RHip"},
    # {9,  "RKnee"},
    # {10, "RAnkle"},
    # {11, "LHip"},
    # {12, "LKnee"},
    # {13, "LAnkle"},
    # {14, "REye"},
    # {15, "LEye"},
    # {16, "REar"},
    # {17, "LEar"},
    Arguments:
        data_path: the path to '.npy' data, the shape of data should be (N, C, T, V, M)
        label_path: the path to label
        window_size: The length of the output sequence
        num_person_in: The number of people the feeder can observe in the input sequence
        num_person_out: The number of people the feeder in the output sequence
        debug: If true, only use the first 100 samples
    """

    def __init__(self,
                 data_path,
                 label_path,
                 ignore_empty_sample=True,
                 window_size=-1,
                 num_person_in=5,
                 num_person_out=2):
        self.data_path = data_path
        self.label_path = label_path
        self.window_size = window_size
        self.num_person_in = num_person_in
        self.num_person_out = num_person_out
        self.ignore_empty_sample = ignore_empty_sample

        self.load_data()

    def load_data(self):
        # load file list
        self.sample_name = os.listdir(self.data_path)

        # load label
        label_path = self.label_path
        with open(label_path) as f:
            label_info = json.load(f)

        sample_id = [name.split('.')[0] for name in self.sample_name]
        self.label = np.array([label_info[id]['label_index'] for id in sample_id])
        has_skeleton = np.array([label_info[id]['has_skeleton'] for id in sample_id])

        # ignore the samples which does not has skeleton sequence
        if self.ignore_empty_sample:
            self.sample_name = [s for h, s in zip(has_skeleton, self.sample_name) if h]
            self.label = self.label[has_skeleton]

        # output data shape (N, C, T, V, M)
        self.N = len(self.sample_name)  # sample
        self.C = 3  # channel
        self.T = max_frame  # frame
        self.V = num_joint  # joint
        self.M = self.num_person_out  # person

    def __len__(self):
        return len(self.sample_name)

    def __iter__(self):
        return self

    def __getitem__(self, index):

        # output shape (C, T, V, M)
        # get data
        sample_name = self.sample_name[index]
        sample_path = os.path.join(self.data_path, sample_name)
        with open(sample_path, 'r') as f:
            video_info = json.load(f)

        # fill data_numpy
        final_data = []
        for v, view_info in enumerate(video_info['data'], 1):
            data_numpy = np.zeros((self.C, self.T, self.V, self.num_person_in))
            for frame_info in view_info:
                frame_index = frame_info['frame_index']
                if frame_index >= self.T:
                    break
                for m, skeleton_info in enumerate(frame_info["skeleton"]):
                    if m >= self.num_person_in:
                        break
                    pose = skeleton_info['pose']
                    score = skeleton_info['score']
                    data_numpy[0, frame_index, :, m] = list((np.array(pose[0::2]) / 1920) - 0.5)
                    data_numpy[1, frame_index, :, m] = list((np.array(pose[1::2]) / 1080) - 0.5)
                    data_numpy[2, frame_index, :, m] = score

            data_numpy[0][data_numpy[2] == 0] = 0
            data_numpy[1][data_numpy[2] == 0] = 0

            # get & check label index
            label = video_info['label_index']
            assert (self.label[index] == label)

            # sort by score
            sort_index = (-data_numpy[2, :, :, :].sum(axis=1)).argsort(axis=1)
            for t, s in enumerate(sort_index):
                data_numpy[:, t, :, :] = data_numpy[:, t, :, s].transpose((1, 2,
                                                                        0))
            
            data_numpy = tools.openpose_match(data_numpy)
            data_numpy = data_numpy[:, :, :, 0:self.num_person_out]

            final_data.append(data_numpy)

        final_data = np.concatenate(final_data)
        return final_data, label


def gendata(data_path, label_path,
            data_out_path, label_out_path,
            num_view,
            num_person_in=num_person_in,  # observe the first 5 persons
            num_person_out=num_person_out,  # then choose 2 persons with the highest score
            max_frame=max_frame):
    feeder = Feeder_kinetics(
        data_path=data_path,
        label_path=label_path,
        num_person_in=num_person_in,
        num_person_out=num_person_out,
        window_size=max_frame)

    sample_name = feeder.sample_name
    sample_label = []

    fp = np.zeros((len(sample_name), num_view, max_frame, num_joint, num_person_out), dtype=np.float32) # 이 부분 지속적으로 변경

    for i, s in enumerate(tqdm(sample_name)):
        data, label = feeder[i]
        if not data.shape[0] == num_view:
            print(s)
            continue
        fp[i, :, 0:data.shape[1], :, :] = data
        sample_label.append(label)

    with open(label_out_path, 'wb') as f:
        pickle.dump((sample_name, list(sample_label)), f)

    np.save(data_out_path, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Kinetics-skeleton Data Converter.')
    parser.add_argument(
        '--data_path', default='../data/kinetics_raw')
    parser.add_argument(
        '--out_folder', default='../data/kinetics')
    arg = parser.parse_args()

    part = ['valid','test', 'train']

    view_list = ['123', '12', '13', '23','1','2','3']
    age_list = ['B', 'C', 'A']
    for age in age_list:
        for view in view_list:
            for p in part:
                print(f'Age: {age}, View: {view}, Use: {p}')
                if not os.path.exists(f'{arg.out_folder}/{view}/{age}/'):
                    os.makedirs(f'{arg.out_folder}/{view}/{age}/')
                data_path = '{}/{}/{}/{}'.format(arg.data_path,view,age, p)
                label_path = '{}/{}/{}/{}_label.json'.format(arg.data_path, view,age, p)
                data_out_path = '{}/{}/{}/{}_data_joint.npy'.format(arg.out_folder,view,age, p)
                label_out_path = '{}/{}/{}/{}_label.pkl'.format(arg.out_folder, view, age, p)

                gendata(data_path, label_path, data_out_path, label_out_path, len(view)*3)