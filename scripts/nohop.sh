#CUDA_VISIBLE_DEVICES = 0
nohup python train.py --cfg_file cfgs/pv_rcnn.yaml > ~/src/ZERONet/pv-rcnn.out 2>&1 &