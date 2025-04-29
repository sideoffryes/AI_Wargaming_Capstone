#!/bin/bash

echo "Creating python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
sleep 2

DIR="$(pwd)"

# Install python environment
echo "Installing python packages..." 
pip install -r requirements.txt
echo "Testing for GPU..."
if python -c "import torch; print(torch.cuda.is_available())" | grep True; then
    echo "GPU detected!"
    pip install faiss-gpu-cu12 bitsandbytes torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu126
else
    echo "No GPU detected!"
    pip install faiss-cpu torch torchvision torchaudio
fi

# HuggingFace login
if [ -s "$HOME/.huggingface/token" ]; then
    echo "✅ Hugging Face credentials found."
else
    echo "⚠️ No Hugging Face credentials found. Running huggingface-cli login..."
    huggingface-cli login
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

# Generate document embeddings
echo ""
read -p "Would you like to generate the document embeddings now? [Y/n] " opt
case "$opt" in
    Y|y|Yes|yes)
        echo "Downloading documents..."
        
        # NAVADMINS
        echo "Downloading NAVADMINS..."
        cd "$DIR"
        bash ./dataDownload.sh
        echo -e "\nNAVADMINS download complete!"

        # MARADMINS
        echo "Downloading MARADMINS..."
        cd "$DIR/capstone"
        python3 MarPull.py
        echo -e "\nMARADMINS download complete!"
        
        # Embeddings
        echo -e "\nGenerating document embeddings..."
        cd "$DIR/capstone"
        python3 embed.py -d all
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
        cd "$DIR/capstone"
        python3 app.py
        ;;
    *)
        echo -e "\nSetup complete!"
        echo "Run 'source .venv/bin/activate' to activate the virtual python environment!"
        ;;
esac