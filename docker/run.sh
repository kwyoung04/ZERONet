docker run  -it \
            -d \
            --gpus all \
            -v /home/ubuntu/eric/OpenPCDet:$HOME/src/OpenPCDet\
            -v /media/data_e/pcdetData/:$HOME/pcdetData\
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name $2 \
            $1 \
            /bin/bash