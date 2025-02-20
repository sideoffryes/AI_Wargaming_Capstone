import faiss, os, argparse
from tqdm import tqdm
import numpy as np
from transformers import AutoModel, AutoTokenizer, logging

logging.set_verbosity_error()

def cache_faiss(chunks: str, fname="./data/NAVADMINS/cache.faiss"):
    """Converts each of the given text chunks into a vectory representation, adds them to a FAISS index, and writes the FAISS index to the disk.

    :param chunks: List of strings to be converted to vectors
    :type chunks: list
    :param fname: path to save FAISS index to, defaults to "./data/NAVADMINS/cache.faiss"
    :type fname: str, optional
    """
    index_file = fname
    embed_file = fname.replace(".faiss", ".npy")
    
    chunk_embeds = []
    for c in tqdm(chunks, desc="Generating document embeddings"):
        chunk_embeds.append(gen_embeds(c).cpu().detach().numpy().flatten())
        
    # chunk_embeds = [gen_embeds(c).cpu().detach().numpy().flatten() for c in chunks]
    chunk_embeds = np.vstack(chunk_embeds)
    
    # normalize for cosine similarity
    faiss.normalize_L2(chunk_embeds)
    
    # create and train faiss index
    index = faiss.IndexFlatIP(chunk_embeds.shape[1])
    index.add(chunk_embeds)
    
    faiss.write_index(index, index_file)
    np.save(embed_file, chunk_embeds)
    
def gen_embeds(text: str):
    """Converts the given string to its vector embedding

    :param text: The text to convert
    :type text: str
    :return: vector of the text
    :rtype: vector
    """
    tokenizer = AutoTokenizer.from_pretrained("princeton-nlp/sup-simcse-roberta-large")
    model = AutoModel.from_pretrained("princeton-nlp/sup-simcse-roberta-large")
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    # last hidden state shape = [batch_size, tokens, hidden_dim]
    return outputs.last_hidden_state[:, 0, :]

if __name__ == "__main__":
    text = []
    for root, dirs, fnames in os.walk("./data/NAVADMINS/"):
        for f in fnames:
            with open(os.path.join(root, f), 'r') as file:
                try:
                    text.append(file.read())
                except:
                    continue

    cache_faiss(text)