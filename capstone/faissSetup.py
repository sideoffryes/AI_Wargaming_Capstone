import argparse
import os

import faiss
import numpy as np
from docx import Document
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer, logging

logging.set_verbosity_error()

tokenizer = AutoTokenizer.from_pretrained("princeton-nlp/sup-simcse-roberta-large")
model = AutoModel.from_pretrained("princeton-nlp/sup-simcse-roberta-large", device_map="cpu")

def cache_faiss(chunks: str, fname):
    """Converts each of the given text chunks into a vectory representation, adds them to a FAISS index, and writes the FAISS index to the disk.

    :param chunks: List of strings to be converted to vectors
    :type chunks: list
    :param fname: path to save FAISS index to, defaults to "./data/NAVADMINS/cache.faiss"
    :type fname: str, optional
    """
    index_file = fname
    
    chunk_embeds = []
    for c in tqdm(chunks, desc="Generating document embeddings"):
        chunk_embeds.append(gen_embeds(c).cpu().detach().numpy().flatten())
        # chunk_embeds.append(gen_embeds(c))
        
    # chunk_embeds = [gen_embeds(c).cpu().detach().numpy().flatten() for c in chunks]
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
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to("cpu")
    outputs = model(**inputs)
    # last hidden state shape = [batch_size, tokens, hidden_dim]
    return outputs.last_hidden_state[:, 0, :]

def nav():
    text = []
    for root, dirs, fnames in os.walk("./data/NAVADMINS/"):
        for f in fnames:
            try:
                with open(os.path.join(root, f), 'r') as file:
                    content = file.read()
                    subj = content.split("SUBJ/")[1].split("//")[0].rsplit("\n")[0]
                    text.append(subj)
            except:
                os.remove(os.path.join(root, f))
    cache_faiss(text, "./data/NAVADMINS/cache.faiss")

def rtw():
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

if __name__ == "__main__":
    doc = int(input("Select the document type you would like to generate embeddings for.\n1. NAVADMINS\n2. Road to War Briefs\n> "))
    match doc:
        case 1:
            nav()
        case 2:
            rtw()
        case _:
            print("ERROR! You did not selection a valid option. Exiting...")
            exit