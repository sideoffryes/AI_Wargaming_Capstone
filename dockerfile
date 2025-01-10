FROM ubuntu:22.04

WORKDIR /app

SHELL ["/bin/bash", "-c"]

# install updates and apps curl
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y curl wget

# install miniconda
RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
RUN rm ~/miniconda3/miniconda.sh
RUN source ~/miniconda3/bin/activate

# edit path
ENV PATH="$PATH:~/miniconda3/bin/"

RUN conda init --all

# install required python packages through conda
RUN conda create -n capstone
RUN echo "source activate capstone" > ~/.bashrc
ENV PATH="$PATH:/opt/conda/envs/capstone/bin:$PATH"

# Try and install all packages at once
RUN conda install -c conda-forge truststore
RUN conda config --set ssl_verify truststore
RUN conda install -c pytorch -c nvidia -c rapidsai -c conda-forge pytorch torchvision torchaudio pytorch-cuda=12.4 faiss-gpu-raft=1.9.0 transformers 

# # pytorch with GPU - CUDA 12.4
# RUN conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
# # FAISS with GPU (NVIDIA RAFT)
# RUN conda install -c pytorch -c nvidia -c rapidsai -c conda-forge faiss-gpu-raft=1.9.0
# # Hugging face
# RUN conda install -c conda-forge transformers --solver classic --use-feature truststore

# USNA certificate stuff
COPY certs/install-ssl-system.sh /app/certs/
COPY certs/system-certs-5.6-pa.tgz /app/certs/
RUN ./certs/install-ssl-system.sh

# provide hugging face token
RUN --mount=type=secret,id=HUGGING_TOKEN huggingface-cli login --token HUGGING_TOKEN 

# copy over files
COPY ./data /app/data
COPY ./scripts /app/scripts
COPY ./UI /app/UI 