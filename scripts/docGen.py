from transformers import pipeline, logging
import torch
import os
import numpy as np

torch.set_num_threads(32)

generator = pipeline("text-generation", model="meta-llama/Llama-3.2-1B-Instruct")
logging.set_verbosity_error()

# define pieces of prompt
role = "Role: You work for the United States Department of the Navy, and you specialize in writing official military documents using military formatting.\n"

# load in examples for few shot prompting
examples = "Consider the following examples when creating the format for your response.\n"

data_path = "../data"
files = []

# get paths to all example files
for root, dirs, fnames in os.walk(data_path):
    for f in fnames:
        files.append(os.path.join(root, f))
        
# append contents of each file to examples
for f in files:
    with open(f, 'r') as file:
        examples += f"Example:\n {file.read()}\n\n"
        
user_query = input("Input> ")
user_query = "Request: " + user_query

prompt = role + examples + user_query

response = generator(prompt, max_new_tokens = 500)[0]['generated_text'][len(prompt):]
print(response)