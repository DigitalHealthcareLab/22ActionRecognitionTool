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
    
2. Download the raw data from GigaDB and put them into 'data/eval_raw' directory by age.
    
        mkdir data/eval_raw
        mkdir data/eval_raw/A data/eval_raw/B data/eval_raw/C
    
3. Run utils/to_action.py to make action recognition dataset

    If you don't want action recognition, skip this step.

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
        
