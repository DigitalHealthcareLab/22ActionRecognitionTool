#!/bin/bash
python3 main.py --config config/action_recognition_multi/123/A/train_joint.yaml --work-dir work_dir/paper/123/A --seed 100
python3 main.py --config config/action_recognition_multi/12/A/train_joint.yaml --work-dir work_dir/paper/12/A --seed 100
python3 main.py --config config/action_recognition_multi/13/A/train_joint.yaml --work-dir work_dir/paper/13/A --seed 100
python3 main.py --config config/action_recognition_multi/23/A/train_joint.yaml --work-dir work_dir/paper/23/A --seed 100
python3 main.py --config config/action_recognition_multi/1/A/train_joint.yaml --work-dir work_dir/paper/1/A --seed 100
python3 main.py --config config/action_recognition_multi/2/A/train_joint.yaml --work-dir work_dir/paper/2/A --seed 100
python3 main.py --config config/action_recognition_multi/3/A/train_joint.yaml --work-dir work_dir/paper/3/A --seed 100