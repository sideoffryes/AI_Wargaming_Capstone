#!/bin/bash

python3 -m venv .venv
echo "Creating python virtual environment..."
source .venv/bin/activate
sleep 2

DIR="$(pwd)"

# Install python environment
pip install -r requirements.txt

# Compile the documentation
echo "Installing python packages with GPU support..."
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