#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

DIR="$(pwd)"

# Install python environment
read -p "Would like to perform the GPU or CPU setup? [GPU/CPU] " opt
if [ "$opt" == "GPU" ]; then
    pip install -r requirements_gpu.txt
elif [ "$opt" == "CPU" ]; then
    pip install -r requirements_cpu.txt
else
    echo "You did not select a valid option! Only enter GPU or CPU!"
    exit
fi

# Generate document embeddings
echo ""
read -p "Would you like to generate the document embeddings now? [Y/n] " opt
if [ "$opt" == "Y" ] || [ "$opt" == "y" ] || [ "$opt" == "Yes" ] || [ "$opt" == "yes" ]; then
    echo "Downloading documents..."
    bash ./dataDownload.sh
    echo -e "\nDownload complete!"
    echo "Please login to Hugging Face!"
    huggingface-cli login
    echo -e "\nGenerating document embeddings..."
    cd "$DIR/capstone"
    python3 faissSetup.py -d all
else
    echo -e '\nRun "source .venv/bin/activate" to activate the virtual environment!'
fi

# Start webserver
read -p "You you like to start the web server right now? [Y/n] " opt
if [ "$opt" == "Y" ] || [ "$opt" == "y" ] || [ "$opt" == "Yes" ] || [ "$opt" == "yes" ]; then
    echo -e "\nStarting webserver..."
    cd "$DIR/capstone"
    python3 app.py
else
    echo -e "\nCompleting setup..."
    echo 'Run "source .venv/bin/activate" to activate the virtual environment!'
fi