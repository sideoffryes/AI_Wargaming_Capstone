from transformers import pipeline, logging, AutoTokenizer, AutoModel
import torch
from torch.nn.functional import cosine_similarity
import time
import os
import faiss
import numpy as np

torch.set_num_threads(32)

# trying new embeddings
tokenizer = AutoTokenizer.from_pretrained("princeton-nlp/sup-simcse-roberta-large")
model = AutoModel.from_pretrained("princeton-nlp/sup-simcse-roberta-large")

generator = pipeline("text-generation", model="meta-llama/Llama-3.2-1B-Instruct")
logging.set_verbosity_error()

memory = "You work at the United States Naval Academy, and you specialize in answering questions about the rules and regulations. Carefully consider the context given for each prompt when thinking about your answer.\n"

def cache_faiss(chunks, fname="cache.faiss"):
    index_file = fname
    embed_file = fname.replace(".faiss", ".npy")
    
    if os.path.exists(index_file) and os.path.exists(embed_file):
        index = faiss.read_index(index_file)
        chunk_embeds = np.load(embed_file)
    else:
        chunk_embeds = [gen_embeds(c).detach().numpy().flatten() for c in chunks]
        chunk_embeds = np.vstack(chunk_embeds)
        
        # normalize for cosine similarity
        faiss.normalize_L2(chunk_embeds)
        
        # create and train faiss index
        index = faiss.IndexFlatIP(chunk_embeds.shape[1])
        index.add(chunk_embeds)
        
        faiss.write_index(index, index_file)
        np.save(embed_file, chunk_embeds)
    
    return index, chunk_embeds

def load_text(path: str, max_len=25) -> list:
    with open(path, 'r') as file:
        text = file.read()
        text = text.split(" ")
        chunks = [" ".join(text[i:i+max_len]) for i in range(0, len(text), max_len)]

    return chunks

def gen_embeds(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :]

def find_most_rel(query, index, top_k=5):
    query_embed = gen_embeds(query).detach().numpy().flatten().reshape(1, -1)
    faiss.normalize_L2(query_embed)
    _, top_k_indices = index.search(query_embed, top_k)
    return top_k_indices[0]

def clean_answer(text: str) -> str:
    text = text.rsplit("\n")[0]
    
    if "Answer> " not in text[:len("Answer> ")] or "Answer: " not in text[:len("Answer: ")]:
        text = "Answer> " + text
    
    period_index = text.rfind(".")
    exc_index = text.rfind("!")
    q_index = text.rfind("?")

    max_index = max(period_index, exc_index, q_index)

    if max_index == period_index:
        return text.rsplit(".")[0] + "."
    elif max_index == exc_index:
        return text.rsplit("!")[0] + "!"
    elif max_index == q_index:
        return text.rsplit("?")[0] + "?"
    else:
        return text

def gen_answer(rel_chunks: list, query: str) -> str:
    global memory
    context = " ".join(rel_chunks)
    prompt = f"Read the following context carefully and use it to answer the question at the end of the prompt: {context}\nAnswer the following prompt: {query}\n"
    memory += prompt
    answer = generator(memory, max_new_tokens=75)[0]['generated_text'][len(memory):]
    answer = clean_answer(answer)
    memory += f"{answer}\n"
    return answer

def cache(chunks, fname="cache.pt"):
    if os.path.exists(fname):
        chunk_embeds = torch.load(fname)
    else:
        t_start = time.time()
        chunk_embeds = [gen_embeds(c) for c in chunks]
        t_stop = time.time()
        t_chunks = t_stop - t_start
        print(f"Generate chunk embeddings: {t_chunks}")
        torch.save(chunk_embeds, fname)
    return chunk_embeds

def rag(chunks: list, query: str) -> str:
    index, chunk_embeds = cache_faiss(chunks)
    top_k_indices = find_most_rel(query, index)
    rel_chunks = [chunks[i] for i in top_k_indices]
    
    # DEBUG
    print(f"-----CHUNKS IDENTIFIED FOR CONTEXT-----")
    counter = 1
    for c in rel_chunks:
        print(f"{counter}. {c}\n")
        counter += 1
    
    t_start = time.time()
    answer = gen_answer(rel_chunks, query)
    t_stop = time.time()
    t_gen = t_stop - t_start
    
    print(f"----- Runtimes -----\nGenerating Llama output: {t_gen}")
    
    return answer

if __name__ == "__main__":
    chunks = load_text("data/midregs.txt")
    user_query = input("Input> ")
    while "quit" not in user_query.lower():
        print(f"\n{rag(chunks, user_query)}\n")
        user_query = input("Input> ")