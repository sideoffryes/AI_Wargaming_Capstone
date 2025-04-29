import json
import os
from argparse import ArgumentParser

import faiss
import numpy as np
from docx import Document
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

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

def nav() -> tuple[list[tuple[str, str]], list[str]]:
    """Returns a list of tuples of NAVADMIN file names and their contents and a list of file paths of NAVADMINS that cannot be read and should be removed

    :return: A list of tuples of files and their contents and a list of files to be removed
    :rtype: tuple[list[tuple[str, str]], list[str]]
    """
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

def mar() -> tuple[list[tuple[str, str]], list[str]]:
    """Returns a list of tuples of MARADMIN file names and their contents and a list of file paths of MARADMINS that cannot be read and should be removed

    :return: A list of tuples of files and their contents and a list of files to be removed
    :rtype: tuple[list[tuple[str, str]], list[str]]
    """
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

def opord() -> tuple[list[tuple[str, str]], list[str]]:
    """Returns a list of tuples of OPORD paragraph file names and their contents and a list of file paths of OPORD paragraphs that cannot be read and should be removed

    :return: A list of tuples of files and their contents and a list of files to be removed
    :rtype: tuple[list[tuple[str, str]], list[str]]
    """
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

def rtw() -> tuple[list[tuple[str, str]], list[str]]:
    """Returns a list of tuples of Road to War Brief file names and their contents and a list of file paths of RTW briefs that cannot be read and should be removed

    :return: A list of tuples of files and their contents and a list of files to be removed
    :rtype: tuple[list[tuple[str, str]], list[str]]
    """
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
    """Returns a list examples to be used matching the provided document type

    :param doc_type: The type of document to return examples of
    :type doc_type: str
    :return: A list of examples of the specified document
    :rtype: list[str]
    """
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

def embed(docs: list[str], model, batch_size: int) -> tuple:
    """Embeds a list of strings in batches

    :param docs: A list of text to be embedded
    :type docs: list[str]
    :param model: The LLM to use to generate the embeddings
    :type model: SentenceTransformer
    :param batch_size: Number of documents to embed at once
    :type batch_size: int
    :return: Numpy vstack of the embeddings and a json object of the corresponding document metadata
    :rtype: tuple
    """
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
    """Builds and returns FAISS index

    :param embeds: Embeddings to be placed into the index
    :type embeds: Numpy vstack
    :return: FAISS Index
    :rtype: FAISS Index
    """
    dim = embeds.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeds)
    return index

def main(doc_type: str):
    # Load examples
    docs = load_examples(doc_type)
    
    # Generate embeddings
    model = SentenceTransformer(EMBED_MODEL, device=None)
    
    # Generate embeddings
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
    
    if args.doc == "all":
        main("nav")
        main("mar")
        main("opord")
        main("rtw")
    else:
        main(args.doc)