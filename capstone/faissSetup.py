import faiss, os, argparse
from tqdm import tqdm
import numpy as np
from transformers import AutoModel, AutoTokenizer, logging

logging.set_verbosity_error()

def cache_faiss(chunks, fname="./data/NAVADMINS/cache.faiss"):
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
            try:
                with open(os.path.join(root, f), 'r') as file:
                    text.append(file.read())
            except:
                os.remove(os.path.join(root, f))

    cache_faiss(text)