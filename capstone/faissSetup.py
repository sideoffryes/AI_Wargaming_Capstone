import os

import faiss
import numpy as np
from docx import Document
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer, logging
from argparse import ArgumentParser
import torch

logging.set_verbosity_error()

tokenizer = AutoTokenizer.from_pretrained("WhereIsAI/UAE-Large-V1")
model = AutoModel.from_pretrained("WhereIsAI/UAE-Large-V1", device_map="cuda")

def cache_faiss(chunks: str, fname):
    """Converts each of the given text chunks into a vectory representation, adds them to a FAISS index, and writes the FAISS index to the disk.

    :param chunks: List of strings to be converted to vectors
    :type chunks: list
    :param fname: path to save FAISS index to"
    :type fname: str, optional
    """
    index_file = fname
    
    chunk_embeds = []
    torch.cuda.empty_cache()
    for c in tqdm(chunks, desc="Generating document embeddings"):
        chunk_embeds.append(gen_embeds(c).cpu().detach().numpy())
        
    chunk_embeds = np.vstack(chunk_embeds)
    
    # normalize for cosine similarity
    faiss.normalize_L2(chunk_embeds)
    
    # create and train faiss index
    index = faiss.IndexFlatIP(chunk_embeds.shape[1])
    index.add(chunk_embeds)
    
    faiss.write_index(index, index_file)
    
def gen_embeds(text: str):
    """Converts the given string to its vector embedding

    :param text: The text to convert
    :type text: str
    :return: vector of the text
    :rtype: vector
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to("cuda")
    outputs = model(**inputs)
    # last hidden state shape = [batch_size, tokens, hidden_dim]
    return outputs.last_hidden_state[:, 0, :]

def nav():
    """Creates vector embeddings for all documents in the data/NAVADMINS/ directory and adds them to FAISS index in same directory.
    """
    text = []
    for root, dirs, fnames in os.walk("./data/NAVADMINS/"):
        for f in fnames:
            if f == "pages.txt":
                continue
            else:
                try:
                    with open(os.path.join(root, f), 'r', errors="ignore") as file:
                        content = file.read()
                        subj = content.split("SUBJ/")[1].split("//")[0].rsplit("\n")[0]
                        text.append(subj)
                except Exception as e:
                    os.remove(os.path.join(root, f))
    cache_faiss(text, "./data/NAVADMINS/cache.faiss")

def mar():
    """Creates vector embeddings for all documents in the data/MARADMINS/ directory and adds them to FAISS index in same directory.
    """
    text = []
    for root, dirs, fnames in os.walk("./data/MARADMINS/"):
        for f in fnames:
            try:
                with open(os.path.join(root, f), 'r', errors="ignore") as file:
                    content = file.read()
                    subj = content.split("SUBJ/")[1]
                    try:
                        subj = subj.split("//")[0].rsplit("\n")[0]
                    except:
                        subj = subj.rsplit("\n")[0]
                    text.append(subj)
            except Exception as e:
                os.remove(os.path.join(root, f))
    cache_faiss(text, "./data/MARADMINS/cache.faiss")

def rtw():
    """Creates vector embeddings for all documents in the data/RTW/ directory and adds them to FAISS index in the same directory.
    """
    text = []
    for root, dirs, fnames in os.walk("./data/RTW/"):
        for f in fnames:
            try:
                doc = Document(os.path.join(root, f))
                body = ""
                for p in doc.paragraphs:
                    body += p.text
                text.append(body)
            except:
                os.remove(os.path.join(root, f))
                
    cache_faiss(text, "./data/RTW/cache.faiss")

def opord():
    """Creates vector embeddings for all documents in the data/OpOrds directory and adds them to FAISS index in the same directory.
    """
    text = []
    for root, dirs, fnames in os.walk("./data/OpOrds/"):
        for f in fnames:
            try:
                with open(os.path.join(root, f), 'r') as file:
                    content = file.read()
                    text.append(content)
            except:
                os.remove(os.path.join(root, f))
                
    cache_faiss(text, "./data/OpOrds/cache.faiss")

if __name__ == "__main__":
    parser = ArgumentParser(prog="faissSetup", description="Generates vector embeddings for different document types")
    parser.add_argument("-d", "--doc", default="nav", help="Document type to generate embeddings. Options are NAVADMIN, MARADMIN, OPORD, Road to War Brief, and all", choices=['nav', 'mar', 'rtw', 'opord', 'all'], required=True)
    args = parser.parse_args()

    match args.doc:
        case "nav":
            nav()
        case "mar":
            mar()
        case "opord":
            opord()
        case "rtw":
            rtw()
        case "all":
            nav()
            mar()
            opord()
            rtw()
        case _:
            print("ERROR! Invalid option selected. Exiting...")
            exit(1)