FROM continuumio/miniconda3

WORKDIR /app

SHELL ["/bin/bash", "-c"]

ARG home

# install all updates and necessary libraries
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y curl wget

# install python AI libraries w/ GPU support
RUN conda create -n capstone -c pytorch -c nvidia -c rapidsai -c conda-forge pytorch torchvision torchaudio pytorch-cuda=12.4 faiss-gpu-raft=1.9.0 transformers huggingface_hub[cli]

# set environment to new env
RUN echo "conda activate capstone" >> ~/.bashrc

# USNA cert stuff
COPY certs/install-ssl-system.sh /app/certs/
COPY certs/system-certs-5.6-pa.tgz /app/certs/
RUN ./certs/install-ssl-system.sh

SHELL ["conda", "run", "-n", "capstone", "/bin/bash", "-c"]

# provide hugging face token
RUN --mount=type=secret,id=hugging_token \
export HUGGING_TOKEN=$(cat /run/secrets/hugging_token | cut -d '=' -f2) && \
huggingface-cli login --token $HUGGING_TOKEN 

# copy over files
COPY ./data /app/data
COPY ./scripts /app/scripts
COPY ./UI /app/UI
# ADD $home/.cache/huggingface/hub /app/.cache/

# set cache ENV variable
# ENV HF_HOME=/app/.cache