#!/bin/bash

cd ~

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install git
sudo apt-get -y install gcc
sudo apt-get -y install make
sudo apt-get -y install unzip
sudo apt-get -y install python-pip


#Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo dpkg -i cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
sudo apt-get update
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update

# Install NVIDIA driver
sudo apt-get install --no-install-recommends nvidia-driver-430
# Reboot. Check that GPUs are visible using the command: nvidia-smi

# Install development and runtime libraries (~4GB)
sudo apt-get install --no-install-recommends \
    cuda-10-1 \
    libcudnn7=7.6.4.38-1+cuda10.1  \
    libcudnn7-dev=7.6.4.38-1+cuda10.1


# Install TensorRT. Requires that libcudnn7 is installed above.
sudo apt-get install -y --no-install-recommends libnvinfer6=6.0.1-1+cuda10.1 \
    libnvinfer-dev=6.0.1-1+cuda10.1 \
    libnvinfer-plugin6=6.0.1-1+cuda10.1


# Darknet
git clone https://github.com/pjreddie/darknet
cd darknet
wget https://pjreddie.com/media/files/darknet53.conv.74
sed -i 's/GPU=.*/GPU=1/' Makefile
sed -i 's/CUDNN=.*/CUDNN=1/' Makefile
sed -i -e 's/        if(i%10000==0 || (i < 1000 && i%100 == 0)){/        if(i%400==0){/g' ./examples/detector.c
sed -i -e "s|#lib = CDLL(\"/home/pjreddie/documents/darknet/libdarknet.so\", RTLD_GLOBAL)|lib = CDLL(\"$HOME/darknet/libdarknet.so\", RTLD_GLOBAL)|g" ./python/darknet.py
sed -i -e "s|lib = CDLL(\"libdarknet.so\", RTLD_GLOBAL)|#lib = CDLL(\"libdarknet.so\", RTLD_GLOBAL)|g" ./python/darknet.py
make

# Protoc
cd ~
curl -OL https://github.com/google/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip
unzip protoc-3.4.0-linux-x86_64.zip -d protoc3
sudo mv protoc3/bin/* /usr/local/bin/
sudo mv protoc3/include/* /usr/local/include/

# Tensorflow
cd ~
sudo apt -y install python3-dev python3-pip
sudo pip3 install -U virtualenv  # system-wide install
virtualenv --system-site-packages -p python3 ./venv_py3
source ./venv_py3/bin/activate  # sh, bash, ksh, or zsh
pip install --upgrade pip
pip install --upgrade tensorflow-gpu
pip install pandas
pip install lxml
pip install pillow
pip install opencv-python
pip install matplotlib

# Tensorflow object detection API
cd ~
git clone https://github.com/tensorflow/models.git
cd models/research
python setup.py build
python setup.py install
sed -i -e 's/          eval_config, category_index.values(), eval_dict)/          eval_config, list(category_index.values()), eval_dict)/g' ./object_detection/model_lib.py
sed -i '27itf.logging.set_verbosity(tf.logging.INFO)' ./object_detection/model_main.py
pip install pycocotools
echo 'export PYTHONPATH=$PYTHONPATH:~/models/research:~/models/research/slim' >> ~/.bashrc
echo  'protoc -I=$HOME/models/research $HOME/models/research/object_detection/protos/*.proto --python_out=$HOME/models/research' >> ~/.bashrc
















