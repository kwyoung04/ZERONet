#CUDA_VISIBLE_DEVICES = 0
nohup python train.py --cfg_file cfgs/pv_rcnn.yaml > ~/src/ZERONet/log/log_file.out 2>&1 &