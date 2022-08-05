import json
import glob
import argparse
from tqdm import tqdm


view_list = ['123', '12', '13', '23', '1', '2', '3']

def make_label_recognition(path):
    for view in view_list:
        for age in ['A', 'B', 'C']:
            for use in ['train', 'test','valid']:
                print(f'Start... Age {view} {age} {use}')
                file_list = glob.glob(f'{path}/{view}/{age}/{use}/*.json')

                label = {}

                for file in tqdm(file_list):
                    with open(file, 'rb') as f:
                        data = json.load(f)
                    tmp = file.split('/')[-1].split('.')[0]
                    
                    label[tmp] = {'has_skeleton' : True,
                                    'label' : data['label'],
                                    'label_index' : data['label_index']}
                
                with open(f'{path}/{view}/{age}/{use}_label.json', 'wt') as f:
                    json.dump(label, f, ensure_ascii=False)

def make_label_evaluation(path):
    for view in view_list:
        for age in ['A', 'B', 'C']:
            for act in range(1,5):
                    for use in ['train', 'test', 'valid']:
                        print(f'Start... View {view}, Age {age}, Act {act}, Use {use}')
                        file_list = glob.glob(f'{path}/{view}/{age}/{act}/{use}/*.json')

                        label = {}

                        for file in tqdm(file_list):
                            with open(file, 'rb') as f:
                                data = json.load(f)
                            tmp = file.split('/')[-1].split('.')[0]
                            
                            label[tmp] = {'has_skeleton' : True,
                                            'label' : data['label'],
                                            'label_index' : data['label_index']}
                        
                        with open(f'{path}/{view}/{age}/{act}/{use}_label.json', 'wt') as f:
                            json.dump(label, f, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--path')
    parser.add_argument('--model', choices = ['evaluation', 'recognition'])

    args = parser.parse_args()

    if args.model == 'evaluation':
        make_label_evaluation(args.path)
    else:
        make_label_recognition(args.path)
