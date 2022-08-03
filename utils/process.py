import json
import glob
import os
import shutil
import logging
import argparse
import numpy as np
from tqdm import tqdm


child_list = ['A', 'B', 'C']


            

# Remove data with no core skeleton.
def remove_zero(root):

    for child in child_list:
        print(f'Age {child} start...')
        file_list = glob.glob(f'{root}/{child}/*')
        for path in tqdm(file_list):
            with open(path, 'rb') as f:
                data = json.load(f)

            new_data = []

            for frame in data['data']:
                new_skel= []
                for skel in frame['skeleton']:
                    if not skel['pose'][2] == 0:
                        new_skel.append(skel)
                if len(new_skel) == 0:
                    continue
                new_data.append({'frame_index' : frame['frame_index'],
                                'skeleton' : new_skel})

            if len(new_data) == 0:
                if not os.path.exists('dump'):
                    os.makedirs('dump')
                shutil.move(path, f'dump/{path.split("/")[-1]}')
                continue

            data['data'] = new_data
            
            with open(path, 'w') as f:
                json.dump(data, f)



# Sort skeleton by ID
def sort(root):

    for child in child_list:
        file_list = glob.glob(f'{root}/{child}/*')
        print(f'Age {child}, start...')
        for path in tqdm(file_list):

            with open(path, 'rb') as f:
                data = json.load(f)

            new_data = []
            past_frame = {}
            for i, curr_frame in enumerate(data['data'], 1):
                if i == 1:
                    new_data.append({'frame_index' : i,
                                    'skeleton' : curr_frame['skeleton']})
                    past_frame = curr_frame
                    continue
                past_core = [f['pose'][:4] for f in past_frame['skeleton']]
                curr_core = np.array([f['pose'][:4] for f in curr_frame['skeleton']])
                
                sorted_skel = []
                index_list = [j for j in range(len(curr_core))]
                for p_core in past_core:
                    if len(index_list) == 0:
                        break
                    diff = np.sum(np.abs(curr_core - p_core), axis = 1)
                    idx = index_list.pop(diff.argmin())
                    curr_core = np.delete(curr_core, diff.argmin(), axis=0)
                    sorted_skel.append(curr_frame['skeleton'][idx])

                if len(index_list) > 0:
                    for idx in index_list:
                        sorted_skel.append(curr_frame['skeleton'][idx])
                
                new_data.append({'frame_index': i,
                                'skeleton' : sorted_skel})
                
                past_frame = curr_frame

            data['data'] = new_data

            with open(path, 'w') as f:
                json.dump(data, f)
            


# Label Checking
def label_check():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('label.txt')
    logger.addHandler(file_handler)

    for child in child_list:
        for act in range(1,5):
            logger.info(f'Age: {child}, Action: {act}')
            logger.info(f'       Total    1    2    3    4')
            a_tot = 0
            b_tot = 0
            c_tot = 0
            d_tot = 0

            for use in ['train','test','valid']:
                file_path = f'123/{child}/{act}/{use}_label.json'
                with open(file_path, 'rb') as f:
                    data = json.load(f)
                A = 0
                B = 0
                C = 0
                D = 0
                for n, d in data.items():
                    if d['label_index'] == 0:
                        A += 1
                    elif d['label_index'] == 1:
                        B += 1
                    elif d['label_index'] == 2:
                        C += 1
                    else:
                        print(f'file {n} has wrong label')
                
                logger.info(f'{use:<7s}{len(data):>5d}{A:>5d}{B:>5d}{C:>5d}')
                a_tot += A
                b_tot += B
                c_tot += C
            
            logger.info(f'       Total{a_tot:>5d}{b_tot:>5d}{c_tot:>5d}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--function')
    parser.add_argument('--path', default = '.')
    args = parser.parse_args()

    function = args.function
    root = args.path

    # Order: remove_zero -> sort

    if function == 'remove_zero':
        remove_zero(root)
    elif function == 'sort':
        sort(root)
    elif function == 'label_check':
        label_check()
    else:
        print('Unknown command.')





            

        

