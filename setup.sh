#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
sleep 2

DIR="$(pwd)"

# Install python environment
read -p "Would you like to perform the GPU or CPU setup? [GPU/CPU] " opt
if [ "$opt" == "GPU" ]; then
    pip install -r requirements_gpu.txt
elif [ "$opt" == "CPU" ]; then
    pip install -r requirements_cpu.txt
else
    echo "You did not select a valid option! Only enter GPU or CPU!"
    exit
fi

# Compile the documentation
read -p "Would you like to compile the documentation? [Y/n] " opt
case "$opt" in
    Y|y|Yes|yes)
        echo "Compiling the HTML documentation..."
        cd "$DIR/docs"
        make html
        echo -e "\nDocs compilation complete!"
        ;;
    *)
        ;;
esac

if [ "$opt" == "Y" ] || [ "$opt" == "y" ] || [ "$opt" == "Yes" ] || [ "$opt" == "yes" ]; then
    echo "Compiling the HTML documentation..."
    cd "$DIR/docs"
    make html
    echo -e "\nDocs compilation complete!"
fi

# Generate document embeddings
echo ""
read -p "Would you like to generate the document embeddings now? [Y/n] " opt
case "$opt" in
    Y|y|Yes|yes)
        echo "Downloading documents..."
        cd "$DIR"
        bash ./dataDownload.sh
        echo -e "\nDownload complete!"
        echo "Please login to Hugging Face!"
        huggingface-cli login
        echo -e "\nGenerating document embeddings..."
        cd "$DIR/capstone"
        python3 faissSetup.py -d all
        ;;
    *)
        echo -e '\nMake sure you generate the embeddings using the faissSetup.py script in the capstone directory before attempting to generate any documents!'
        ;;
esac

# Start webserver
read -p "You you like to start the web server right now? [Y/n] " opt
case "$opt" in
    Y|y|Yes|yes)
        echo -e "\nStarting webserver..."
        cd "$Dir/capstone"
        python3 app.py
        ;;
    *)
        echo -e "\nSetup complete!"
        echo "Run 'source .venv/bin/activate' to activate the virtual python environment!"
        ;;
esac