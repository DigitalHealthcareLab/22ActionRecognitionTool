import os
import shutil
import glob
import argparse
import json
import random


random.seed(100)
age_list = ['A', 'B', 'C']

def split(x):

    '''
    Split train/valid/test by 8:1:1
    If you want to change the ratio, change the parameters in train_cnt and test_cnt variable definition code.
    '''

    total = len(x)
    train_cnt = round(total*0.8)
    test_cnt = train_cnt + round((total-train_cnt)/2)
    random.shuffle(x)
    train_list = x[:train_cnt]
    test_list = x[train_cnt:test_cnt]
    valid_list = x[test_cnt:]

    return train_list, test_list, valid_list



def main_recognition(path):
    for age in age_list:
        for use in ['train', 'test', 'valid']:
                os.makedirs(f'{path}/{age}/{use}', exist_ok = True)
        child_list = list(set([f.split('/')[-1].split('_')[0] for f in glob.glob(f'{path}/{age}/*.json')]))

        A = []
        B = []
        C = []
        D = []

        for child in child_list:
            file = glob.glob(f'{path}/{age}/{child}*.json')[0]

            with open(file, 'rb') as f:
                data = json.load(f)
            
            if data['label_index'] == 0:
                A.append(child)
            elif data['label_index'] == 1:
                B.append(child)
            elif data['label_index'] == 2:
                C.append(child)
            elif data['label_index'] == 3:
                D.append(child)
            else:
                print(f'Unknown label. /n Code: {child}')



        for X in [A,B,C,D]:
            train, test, valid = split(X)
            for child in train:
                file_list = glob.glob(f'{path}/{age}/{child}*.json')
                for f in file_list:
                    target = os.path.join(f'{path}/{age}/', 'train',f.split('/')[-1])
                    shutil.move(f, target)
            for child in test:
                file_list = glob.glob(f'{path}/{age}/{child}*.json')
                for f in file_list:
                    target = os.path.join(f'{path}/{age}/', 'test',f.split('/')[-1])
                    shutil.move(f, target)
            for child in valid:
                file_list = glob.glob(f'{path}/{age}/{child}*.json')
                for f in file_list:
                    target = os.path.join(f'{path}/{age}/', 'valid',f.split('/')[-1])
                    shutil.move(f, target)

def main_evaluation(path):
    for age in age_list:
        for act in range(1,5):
            for use in ['train', 'test', 'valid']:
                    os.makedirs(f'{path}/{age}/{act}/{use}', exist_ok = True)
            child_list = list(set([f.split('/')[-1].split('_')[0] for f in glob.glob(f'{path}/{age}/*GMS_{act}_*.json')]))

            A = []
            B = []
            C = []
            D = []

            for child in child_list:
                file = glob.glob(f'{path}/{age}/{child}_GMS_{act}*.json')[0]

                with open(file, 'rb') as f:
                    data = json.load(f)
                
                if data['label_index'] == 0:
                    A.append(child)
                elif data['label_index'] == 1:
                    B.append(child)
                elif data['label_index'] == 2:
                    C.append(child)
                elif data['label_index'] == 3:
                    D.append(child)
                else:
                    print(f'Unknown label. /n Code: {child}')



            for X in [A,B,C,D]:
                train, test, valid = split(X)
                for child in train:
                    file_list = glob.glob(f'{path}/{age}/{child}_GMS_{act}*.json')
                    for f in file_list:
                        target = os.path.join(f'{path}/{age}/{act}/', 'train',f.split('/')[-1])
                        shutil.move(f, target)
                for child in test:
                    file_list = glob.glob(f'{path}/{age}/{child}_GMS_{act}*.json')
                    for f in file_list:
                        target = os.path.join(f'{path}/{age}/{act}/', 'test',f.split('/')[-1])
                        shutil.move(f, target)
                for child in valid:
                    file_list = glob.glob(f'{path}/{age}/{child}_GMS_{act}*.json')
                    for f in file_list:
                        target = os.path.join(f'{path}/{age}/{act}/', 'valid',f.split('/')[-1])
                        shutil.move(f, target)


if __name__ == '__main__':
    

    parser = argparse.ArgumentParser()

    parser.add_argument('--path', type = str)
    parser.add_argument('--model', choices = ['evaluation', 'recognition'])

    args = parser.parse_args()

    if args.model == 'evaluation':
        main_evaluation(args.path)
    else:
        main_recognition(args.path)

