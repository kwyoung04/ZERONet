ARG PYTORCH="1.10.0"
ARG CUDA="11.3"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0+PTX"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True



RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

RUN apt update
RUN apt install -y \
    vim \
    sudo \
    gedit \
    libboost-all-dev \
    libssl-dev \
    python3-setuptools \
    git 


################ python 3.8    ################
RUN apt install -y python3.8-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN apt install -y python3-pip
RUN pip3 install --upgrade pip

ADD connection.py /usr/lib/python3.8/multiprocessing


################ spconv   ################
RUN pip install spconv-cu111

################ waymodataset ################
RUN pip install waymo-open-dataset-tf-2-5-0

################ OpenPCDet at git ################
RUN pip install llvmlite \
                 numba \
                 tensorboardX \
                 easydict \
                 pyyaml \
                 scikit-image \
                 tqdm
RUN pip install numpy==1.19.2 \
                 SharedArray==3.1.0 \
                 torch_scatter

################ user setting ################
RUN apt update
RUN apt install -y sudo

ARG  HOST_USER=eric
ARG  UNAME=${HOST_USER}
ARG  HOME=/home/${UNAME}
ARG  MAINPC_IP=localhost
ARG  UID=1000
ARG  GID=1000

RUN  groupadd --system --gid ${GID} ${UNAME} \
 &&  useradd -rm -d ${HOME} -s /bin/bash -g root -G sudo,audio,video,plugdev -u ${UID} ${UNAME} \
 &&  usermod -aG dialout ${UNAME} \
 &&  usermod -aG sudo ${UNAME} \
 &&  mkdir -p /etc/sudoers.d \
 &&  echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${UNAME} \
 &&  chmod 0440 /etc/sudoers.d/${UNAME} 

USER  ${UNAME}
WORKDIR  $HOME