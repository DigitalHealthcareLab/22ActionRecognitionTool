# 22ActionRecognitionTool

## Multi-view child motor development dataset for AI-driven assessment of child development 


<img src= "https://user-images.githubusercontent.com/74819176/182763597-7c774c29-261e-4a2c-9057-83da7f72cad4.jpeg" width = 360 height = 272>

## Guide
### We use the MS-G3D model for this project

    @inproceedings{liu2020disentangling,
      title={Disentangling and Unifying Graph Convolutions for Skeleton-Based Action Recognition},
      author={Liu, Ziyu and Zhang, Hongwen and Chen, Zhenghao and Wang, Zhiyong and Ouyang, Wanli},
      booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
      pages={143--152},
      year={2020}
    }

More details about model are in MS-G3D github : https://github.com/kenziyuliu/MS-G3D

-------------
## Prerequisite
PyTorch >= 3.6
After install the torch, install others.

    pip install -r requirements.txt

--------------
## Data preparation & Model Learning
### Before
1. git clone this depository.

        git clone https://github.com/DigitalHealthcareLab/22ActionRecognitionTool.git
    
2. Download the raw data:

    Skeleton coordinates data 
    
    Age group A: https://drive.google.com/file/d/1mz76H9JAqcKAESGbhcIS_545jD9RtZak/view?usp=sharing
    
    Age group B: https://drive.google.com/file/d/1bJsfE1qzTDHvb2YLmLKnGQuKGGP0AM8Z/view?usp=sharing
    
    Age group C: https://drive.google.com/file/d/15oE8yif2GE71b5llicAtPcp7HyRFOkA9/view?usp=sharing
    
    Skeleton video
    
    Age group A: https://drive.google.com/file/d/1KYbY1FWY1Cl4P8CnxdTtFUNhd55Yr1UM/view?usp=sharing
    
    Age group B: https://drive.google.com/file/d/1-2WvMgR4BTwIffb7aLdL1R0RNast3qpT/view?usp=sharing
    
    Age group C: https://drive.google.com/file/d/1Yqj3KEX6i2ykoH7EjJhP7veycZpiI36_/view?usp=sharing

3. Put them into 'data/eval_raw' directory and unzip.
    
4. Run utils/to_action.py to make action recognition dataset

    If you don't need action recognition, skip this step.

        cd utils
        python3 to_action.py --data_path ../data/eval_raw --out_path ../data/recog_raw
    

### Action Evaluation

- Data preprocessing
    
        cd utils
        python3 train_test_split.py --path ../data/eval_raw --model evaluation
        python3 make_label.py --path ../data/eval_raw --model evaluation
        cd ../data_gen
        python3 evaluation_gendata.py --data_path ../data/eval_raw --out_folder ../data/evaluation

- Train

    Run main.py to train the models by age and action number.
    
    If you got Out of Memory error, change the batch size in config file.
    
        python3 main.py --config config/action_evaluation/[age]/[act_num]/train_joint.yaml --work-dir work_dir/evaluation/[age]/[act_num] --seed 100

- Test

    After train, there is the best epoch number in 'work_dir/evaluation/[age]/[act_num]/log.txt'.
    
    Following this, fix the weight path in 'config/action_evaluation/[age]/[act_num]/test_joint.yaml'
    
    Then run main.py again.
    
        python3 main.py --config config/action_evaluation/[age]/[act_num]/test_joint.yaml --work-dir test_result/evaluation/[age]/[act_num]
    

### Action Recognition

- Data preprocessing

        cd utils
        python3 train_test_split.py --path ../data/recog_raw --model recognition
        python3 make_label.py --path ../data/recog_raw --model recognition
        cd ../data_gen
        python3 recognition_gendata.py --data_path ../data/recog_raw --out_folder ../data/recognition

- Train

    Run main.py to train by age.
    
    If you got Out of Memory error, change the batch size in config file.
    
        python3 main.py --config config/action_recognition/[age]/train_joint.yaml --work-dir work_dir/recognition/[age] --seed 100
        
- Test

    After train, fix the weight path in config file and run main.py again.
    
        python3 main.py --config config/action_recognition/[age]/test_joint.yaml --work-dir test_result/recognition/[age]

---------------
### Paper Replication

If you want to replicate our experiment, follow this.

- Data download

    This is the filtered version of our dataset that has all three views.
    
    Data with only two or one view has been removed.

    Age group A: https://drive.google.com/file/d/1Qaj3OBg2JuoYMUGMP5DaGZakQuFlVJTM/view?usp=sharing
    
    Age group B: https://drive.google.com/file/d/1hLadvFISnWc_yNaV7rn-8FEnA4mjDplH/view?usp=sharing
    
    Age group C: https://drive.google.com/file/d/1KUNvMyaUsWj2LdjQl-mmW2Z9JwgVUxas/view?usp=sharing
    
    Unzip and put these into 'data/filtered_raw'.
    
- Data preprocessing

        cd utils
        python3 to_action.py --data_path ../data/filtered_raw --out_path ../recog_filtered_raw
        python3 train_test_split.py --path ../data/recog_raw --model recognition
        python3 split_view.py --data_path ../data/recog_raw --out_path ../data/recog_multi_raw --model recognition
        python3 make_label_multi.py --path ../data/recog_multi_raw --model recognition
        cd ../data_gen
        python3 recognition_gendata_multi.py --data_path ../data/recog_multi_raw --out_folder ../data/recognition_multi
    
- Train

    Run train_A.sh, train_B.sh, train_C.sh one by one.
    
    It will train all view settings automatically.
    
        bash train_A.sh
        bash train_B.sh
        bash train_C.sh

- Test

    After train, fix the weight path in config file and run main.py.
    
        python3 main.py --config config/action_recognition_multi/[view]/[age]/test_joint.yaml --work-dir test_result/recognition_multi/[view]/[age]

-----------
- Repository Author: Jinyong Kim
- Organization: DHLab, Yonsei University
