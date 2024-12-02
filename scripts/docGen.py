from transformers import pipeline, logging
import torch
import os
import time
from datetime import datetime

# torch.set_num_threads(32)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

generator = pipeline("text-generation", model="meta-llama/Llama-3.2-1B-Instruct", device=device)
logging.set_verbosity_error()

def clean_output(text: str) -> str:
    return text.rsplit("Example:")[0]

# get document type from user
doc = int(input("Select document to generate\n1) Naval Message\n2) USMC Message\n> "))
type = ""

match doc:
    case 1:
        type = "NAVADMIN"
    case 2:
        type = "MARADMIN"
    case _:
        type = "NAVADMIN"

# define pieces of prompt
role = "Role: You work for the United States Department of the Navy, and you specialize in writing official military documents using military formatting.\n"

# load in examples for few shot prompting
examples = "Read the following examples very carefully. Your response must follow the same formatting as these examples.\n"

data_path = "../data"
files = []

# get paths to all example files
for root, dirs, fnames in os.walk(data_path):
    for f in fnames:
        if type in f:
            files.append(os.path.join(root, f))

# append contents of each file to examples
for f in files:
    with open(f, 'r') as file:
        examples += f"Example:\n {file.read()}\n\n"
        
user_query = input("Input> ")
user_query = "Request: " + user_query
format = "Give your answer in naval message format based on the previous examples."

prompt = role + examples + user_query + format

t_start = time.time()
response = generator(prompt, max_new_tokens = 500)[0]['generated_text'][len(prompt):]
t_stop = time.time()

# response = clean_output(response)

print(response)
print(f"Generation time: {t_stop - t_start}")

# save response to file
fname = datetime.now().strftime("%d-%b-%Y_%H:%M:%S")
path = f"../output/{fname}.txt"
with open(path, 'w') as file:
    file.write(f"---------- RESPONSE ----------\n{response}\n\n")
    file.write(f"---------- PROMPT ----------\n{prompt}")