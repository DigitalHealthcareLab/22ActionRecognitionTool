import os
import glob
import shutil
from tqdm import tqdm

view_list = ['12', '13', '23', '1', '2', '3']
age_list = ['B','C','D']

# For action evaluation
for age in age_list:
    for act in range(1, 5):
        for use in ['train', 'test', 'valid']:
            file_list = glob.glob(f'123/{age}/{act}/{use}/*')

            for view in view_list:
                print(f'Age: {age}, Action: {act}, Use: {use}, View: {view} start.')
                target_path = f"{view}/{age}/{act}/{use}"
                if not os.path.exists(target_path):
                    os.makedirs(target_path)

                for file in tqdm(file_list):
                    if file.split('_')[-1].split('.')[0] in view:
                        shutil.copy(file, f"{target_path}/{file.split('/')[-1]}")

# For action recognition
# for view in view_list:
#     for age in age_list:
#         print(f'View: {view}, Age: {age} start.')
#         target_path = f"action/{view}/{age}/"
#         if not os.path.exists(target_path):
#             os.makedirs(target_path)

#         file_list = glob.glob(f'action/{age}/*')

#         for file in tqdm(file_list):
#             if file.split('_')[-1].split('.')[0] in view:
#                 shutil.copy(file, f"{target_path}/{file.split('/')[-1]}")
        
        