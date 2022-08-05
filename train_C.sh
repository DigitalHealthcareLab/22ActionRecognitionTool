#!/bin/bash
python3 main.py --config config/action_recognition_multi/123/C/train_joint.yaml --work-dir work_dir/paper/123/C --seed 100
python3 main.py --config config/action_recognition_multi/12/C/train_joint.yaml --work-dir work_dir/paper/12/C --seed 100
python3 main.py --config config/action_recognition_multi/13/C/train_joint.yaml --work-dir work_dir/paper/13/C --seed 100
python3 main.py --config config/action_recognition_multi/23/C/train_joint.yaml --work-dir work_dir/paper/23/C --seed 100
python3 main.py --config config/action_recognition_multi/1/C/train_joint.yaml --work-dir work_dir/paper/1/C --seed 100
python3 main.py --config config/action_recognition_multi/2/C/train_joint.yaml --work-dir work_dir/paper/2/C --seed 100
python3 main.py --config config/action_recognition_multi/3/C/train_joint.yaml --work-dir work_dir/paper/3/C --seed 100