import os
import glob
import shutil
import argparse
from tqdm import tqdm





view_list = ['123', '12', '13', '23', '1', '2', '3']
age_list = ['A', 'B','C']

def split_evalution(data_path, out_path):

    # For action evaluation

    for age in age_list:
        for act in range(1, 5):
            for use in ['train', 'test', 'valid']:
                file_list = glob.glob(f'{data_path}/{age}/{act}/{use}/*')

                for view in view_list:
                    print(f'Age: {age}, Action: {act}, Use: {use}, View: {view} start.')
                    target_path = f"{out_path}/{view}/{age}/{act}/{use}"
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)

                    for file in tqdm(file_list):
                        if file.split('_')[-1].split('.')[0] in view:
                            shutil.copy(file, f"{target_path}/{file.split('/')[-1]}")

def split_recognition(data_path, out_path):

    # For action recognition

    for view in view_list:
        for age in age_list:
            print(f'View: {view}, Age: {age} start.')
            target_path = f"{out_path}/{view}/{age}/"
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            file_list = glob.glob(f'{data_path}/{age}/*')

            for file in tqdm(file_list):
                if file.split('_')[-1].split('.')[0] in view:
                    shutil.copy(file, f"{target_path}/{file.split('/')[-1]}")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path')
    parser.add_argument('--out_path')
    parser.add_argument('--model', choices = ['evaluation', 'recognition'])
    args = parser.parse_args()

    if args.model == 'evaluation':
        split_evalution(args.data_path, args.out_path)
    else:
        split_recognition(args.data_path, args.out_path)

        