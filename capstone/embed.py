from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import numpy as np
import faiss
import json
import os
from argparse import ArgumentParser
from docx import Document

args = None
parser = ArgumentParser(prog="faissSetup", description="Generates vector embeddings for different document types")
parser.add_argument("-d", "--doc", default="nav", help="Document type to generate embeddings. Options are NAVADMIN, MARADMIN, OPORD, Road to War Brief, and all", choices=['nav', 'mar', 'rtw', 'opord', 'all'], required=True)
parser.add_argument("-b", "--batch", default=128, help="Batch size to use when generating document embeddings, default is 128")

EMBED_MODEL = "intfloat/e5-large-v2"
dirs = ["admin_log", "command_sig", "execution", "mission", "orientation", "situation"]

NAV_DIR = "./data/NAVADMINS/"
MAR_DIR = "./data/MARADMINS/"
RTW_DIR = "./data/RTW/"
OPORD_DIR = "./data/OPORDS/"

NAV_META = "./data/NAVADMINS/metadata.json"
MAR_META = "./data/MARADMINS/metadata.json"
RTW_META = "./data/RTW/metadata.json"
OPORD_META = "./data/OPORDS/metadata.json"

NAV_INDEX = "./data/NAVADMINS/index.faiss"
MAR_INDEX = "./data/MARADMINS/index.faiss"
RTW_INDEX = "./data/RTW/index.faiss"
OPORD_INDEX = "./data/OPORDS/index.faiss"

BATCH_SIZE = getattr(args, "batch", 128) 

def nav() -> tuple[list[str], list[str]]:
    docs = []
    broken = []
    for file in os.listdir(NAV_DIR):
        if file.endswith(".txt") and file != "pages.txt":
            path = os.path.join(NAV_DIR, file)
            try:
                with open(path, "r") as f:
                    text = f.read()
                    docs.append((file, text))
            except Exception as e:
                print(f"[WARNING] Could not read {f}: {e}")
                broken.append(path)
                
    return docs, broken

def mar() -> tuple[list[str], list[str]]:
    docs = []
    broken = []
    for file in os.listdir(MAR_DIR):
        if file.endswith(".txt"):
            path = os.path.join(MAR_DIR, file)
            try:
                with open(path, "r") as f:
                    text = f.read()
                    docs.append((file, text))
            except Exception as e:
                print(f"[WARNING] Could not read {f}: {e}")
                broken.append(path)
                
    return docs, broken

def opord() -> tuple[list[str], list[str]]:
    docs = []
    broken = []
    dirs = ["admin_log", "command_sig", "execution", "mission", "orientation", "situation"]

    for d in dirs:
        for file in os.listdir(os.path.join(OPORD_DIR, d)):
            if file.endswith(".txt"):
                path = os.path.join(OPORD_DIR, d, file)
                try:
                    with open(path, 'r') as f:
                        text = f.read()
                        docs.append((file, text))
                except Exception as e:
                    print(f"[WARNING] Could not read {f}: {e}")
                    broken.append(path)
    
    return docs, broken

def rtw() -> tuple[list[str], list[str]]:
    docs = []
    broken = []
    
    for file in os.listdir(RTW_DIR):
        if file.endswith(".docx"):
            path = os.path.join(RTW_DIR, file)
            try:
                doc = Document(path)
                body = ""
                for p in doc.paragraphs:
                    body += p.text
                docs.append((file, body))
            except Exception as e:
                print(f"[WARNING] Could not read {path}: {e}")
                broken.append(path)
        
    return docs, broken

def load_examples(doc_type: str) -> list[str]:
    docs = []
    broken = []
    
    match doc_type:
        case "nav":
            docs, broken = nav()
        case "mar":
            docs, broken = mar()
        case "opord":
            docs, broken = opord()
        case "rtw":
            docs, broken = rtw()
        case _:
            print(f"[ERROR] You did not select a valid document type. Run python3 embed.py -h to see options.")
            exit(1)
    
    # remove broken files
    for path in broken:
        try:
            os.remove(path)
            print(f"[Info] Deleted unreadable file: {path}")
        except Exception as e:
            print(f"[Error]: Failed to delete {path}: {e}")
    
    return docs

def embed(docs: list[str], model, batch_size: int):
    embeds = []
    metadata = []
    j = 0
    for i in tqdm(range(0, len(docs), batch_size), desc="Embedding Documents by Batch"):
        doc_batch = docs[i:i + batch_size]
        doc_text = [doc[1] for doc in doc_batch]
        doc_name = [doc[0] for doc in doc_batch]
        
        doc_embeddings = model.encode(doc_text, normalize_embeddings=True)
        
        embeds.append(doc_embeddings)
        
        for name, text in zip(doc_name, doc_text):
            data = {
                "fname": name,
                "text": text,
                "id": j
            }
            j += 1
            metadata.append(data)

    array = np.vstack(embeds)
    return array, metadata
    
def build_faiss(embeds):
    dim = embeds.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeds)
    return index

def main(doc_type: str):
    # Load examples
    docs = load_examples(doc_type)
    
    # Generate embeddings
    model = SentenceTransformer(EMBED_MODEL)
    embeds, metadata = embed(docs, model, batch_size=BATCH_SIZE)
    
    # Build FAISS index
    index = build_faiss(embeds)
    
    metadata_file = ""
    index_file = ""
    match doc_type:
        case "nav":
            metadata_file = NAV_META
            index_file = NAV_INDEX
        case "mar":
            metadata_file = MAR_META
            index_file = MAR_INDEX
        case "opord":
            metadata_file = OPORD_META
            index_file = OPORD_INDEX
        case "rtw":
            metadata_file = RTW_META
            index_file = RTW_INDEX
        case _:
            print(f"[ERROR] Invalid doc type for writing embedding index and metadata to disk.")
            exit(2)
            
    # Save metadata and index to disk
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
        
    faiss.write_index(index, index_file)

if __name__ == "__main__":
    args = parser.parse_args()
    
    print(f"[INFO] Generating embeddings for {args.doc}")
    
    main(args.doc)