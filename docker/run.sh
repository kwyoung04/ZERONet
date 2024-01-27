docker run  -it \
            -d \
            --gpus all \
            -v /home/ubuntu/eric/ZERONet:$HOME/src/ZERONet\
            -v /data/lidar_zeron/:$HOME/data\
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name openpcd-1.3 \
            eric/openpcdet:1.3 \
            /bin/bash