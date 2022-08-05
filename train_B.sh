#!/bin/bash
python3 main.py --config config/action_recognition_multi/123/B/train_joint.yaml --work-dir work_dir/paper/123/B --seed 100
python3 main.py --config config/action_recognition_multi/12/B/train_joint.yaml --work-dir work_dir/paper/12/B --seed 100
python3 main.py --config config/action_recognition_multi/13/B/train_joint.yaml --work-dir work_dir/paper/13/B --seed 100
python3 main.py --config config/action_recognition_multi/23/B/train_joint.yaml --work-dir work_dir/paper/23/B --seed 100
python3 main.py --config config/action_recognition_multi/1/B/train_joint.yaml --work-dir work_dir/paper/1/B --seed 100
python3 main.py --config config/action_recognition_multi/2/B/train_joint.yaml --work-dir work_dir/paper/2/B --seed 100
python3 main.py --config config/action_recognition_multi/3/B/train_joint.yaml --work-dir work_dir/paper/3/B --seed 100