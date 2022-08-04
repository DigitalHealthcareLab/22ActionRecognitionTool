import json
import glob
import shutil
import os 
import argparse
from tqdm import tqdm



age_list = ['A', 'B','C']

def main(data_path, out_path):
    for age in age_list:
        for act in range(1, 5):
        
            target_path = f"{out_path}/{age}/"
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            print(f'Age: {age}, Action: {act}  start.')

            if age == 'A':
                if act == 1:
                    act_name = 'climb the stairs'
                elif act == 2:
                    act_name = 'go down the stairs'
                elif act == 3:
                    act_name = 'throw the ball'
                else:
                    act_name = 'standing with one leg for 1 sec'
            elif age == 'B':
                if act == 1:
                    act_name = 'standing with one leg for 3 sec'
                elif act == 2:
                    act_name = 'hopping with one leg'
                elif act == 3:
                    act_name = 'long jump'
                else:
                    act_name = 'catching the ball'
            elif age == 'C':
                if act == 1:
                    act_name = 'stopping a rolling ball with foot'
                elif act == 2:
                    act_name = 'bouncing the ball'
                elif act == 3:
                    act_name = 'jumping over the rope'
                else:
                    act_name = 'jump a rope once'
            file_list = glob.glob(f'{data_path}/{age}/*S_{act}*')
            for file in tqdm(file_list):
                with open(file, 'rb') as f:
                    data = json.load(f)
                if data['label_index'] > 0: 
                    data['label_index'] = act - 1
                    data['label'] = act_name
                    with open(f"{target_path}/{file.split('/')[-1]}", 'w') as f:
                        json.dump(data, f, ensure_ascii = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path')
    parser.add_argument('--out_path')
    args = parser.parse_args()
    
    main(args.data_path, args.out_path)

            

