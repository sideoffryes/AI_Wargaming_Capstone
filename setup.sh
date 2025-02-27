#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

read -p "Would like to perform the GPU or CPU setup? " opt

if [[ "$opt" == "GPU" ]]; then
    pip install -r requirements_gpu.txt
elif [[ "$opt" == "CPU" ]]; then
    pip install -r requiremments_cpu.txt
else
    echo "You did not select a valid option! Only enter GPU or CPU!"
    exit
fi

pip install flash-attn --no-build-isolation

bash ./dataDownload.sh
python3 ./capstone/faissSetup.py