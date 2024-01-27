#docker pull kwyoung04/ros_openpcdet:voxelnet

docker run  --net=host \
            -it \
            -d \
            --gpus "device=6" \
            -v /data/lidar_zeron:$HOME/data\
            -v /home/ubuntu/eric/ZERONet:$HOME/src/ZERONet\
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name openpcd6 \
            7aad87a5ecf1  \
            /bin/bash