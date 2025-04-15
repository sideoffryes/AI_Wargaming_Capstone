import argparse
import os
import time
import warnings
from datetime import date, datetime

import faiss
import torch
from docx import Document
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          BitsAndBytesConfig, TextStreamer, logging)

from faissSetup import gen_embeds

warnings.filterwarnings("ignore", category=UserWarning)

# export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

def gen(model_num: int, type_num: int, prompt: str, save: bool = False) -> str:
    """Generates a specificed document using a specified LLM and returns the result.

    :param model_num: The number value representing the model to use for generation.
    :type model_num: int
    :param type_num: The number value representing the type of document to generate.
    :type type_num: int
    :param prompt: The prompting given to the LLM to use for generation.
    :type prompt: str
    :param save: Specifies if the output should be saved to the disk or not, defaults to True
    :type save: bool, optional
    :return: The document produced by the LLM
    :rtype: str
    """
    logging.set_verbosity_error()
    model_name = select_model(model_num)
    doc_type = select_doc(type_num)

    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")

    staff = """The current US military chain of command is:
    President of the United States: Donald Trump
    Vice President of the United States: JD Vance
    Secretary of Defense: Pete Hegseth
    Chairman of the Joint Chiefs of Staff: ADM Christopher Grady, USN, Acting
    Vice Chairman of the Joint Chiefs of Staff: ADM Christopher Grady, USN, Acting
    Chief of Naval Operations: ADM James Kilby, USN, acting
    Chief of Staff of the Army: General Randy George, USA
    Chief of Staff of the Air Force: General David Allvin, USAF
    Commandant of the Marine Corps: General Eric Smith, USMC
    Commandant of the Coast Guard: ADM Kevin Lunday, USCG
    Chief of Space Operations: General Chance Saltzman, USSF
    """

    doc_instructions = ""

    match doc_type:
        case "NAVADMIN":
            doc_instructions = "The document you must write is a NAVADMIN. A NAVADMIN is a Navy Administrative Message used to disseminate information, policies, and instructions. Your response must be in exact NAVADMIN formatting. Your response must both begin and end with the CLASSIFICATION line."
        case "MARADMIN":
            doc_instructions = "The document you must write is a MARADMIN. A MARADMIN is used by Headquarters Marine Corps staff agencies and specific authorized commands to disseminate route and administrative information applicable to all Marines. You response must be in exact MARADMIN formatting."
        case "OpOrd":
            doc_instructions = """An OPORD, Operations Order, or Five Paragraph Order is used to issue an order in a clear and concise manner. There are 5 elements to this order: Situation, Mission, Execution, Administration and Logistics, and Command and Signal. You must write all 5 paragraphs.
            The situation paragraph contains information on the overall status and disposition of both friendly and enemy forces. It contains 3 subparagraphs on enemy forces and friendly forces.
            The mission paragraph provides a clear and concise statement of what the unit must accomplish. This is the heard of the order and must contain the who, what, when, where, and why of the operation.
            The execution paragraph contains the information needed to conduct the operation. It includes 3 subparagraphs on concept of operations, tasks, and coordination instructions.
            The administration and logistics paragraph contains information or instructions pertaining to rations and ammunition, location of the distribution point, corpsman, aid station, handling of prisoners of war, and other matters.
            The command and signal paragraph contains 2 subparagraphs on the chain of command with their location and signal instructions for frequences, call signs, radio procedures, etc.
            """
        case "RTW":
            doc_instructions = "The document you must write is a Road to War Brief. This brief describes the scenario and narrative that sets the stage for a conflict, outlining the events and factors leading up to the conflict."
        case _:
            doc_instructions = ""

    # Set LLM instructions
    role = "Role: You work for the United States Department of Defense, and you specialize in writing official military documents using military formatting.\n"
    task = f"{doc_instructions} Your answer must be a complete document. Do not add any additional content outside of the document. Today's date is {formatted_date}. Adjust the dates in your response accordinly. The following examples are all examples of the same type of document that you must create. Study their formatting carefully before giving your response."
    
    # create model objects
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto", quantization_config=BitsAndBytesConfig(load_in_8bit=True, llm_int8_enable_fp32_cpu_offload=True))
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # set up prompt info
    examples = load_examples(doc_type, prompt)
    
    if doc_type == "OpOrd":
        return opord_gen([prompt, role, staff, task], examples, model, tokenizer)
    else:
        prompt = role + staff + task + examples + "Now that you have studied the examples, create the same type of example using the following prompt: " + prompt
        
        # set device based on gpu availability
        model_inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # generate response
        t_start = time.time()
        generated_ids = model.generate(**model_inputs, do_sample=True, max_new_tokens=1000, eos_token_id=tokenizer.eos_token_id)
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0][len(prompt):]
        t_stop = time.time()
        print(f"Generation time: {t_stop - t_start} sec / {(t_stop - t_start) / 60} min")
        
        if save:
            save_response(response, prompt, model_name, model)
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return response

def opord_gen(prompts: list[str], examples: str, model, tokenizer):
    prompt = prompts[0]
    role = prompts[1]
    staff = prompts[2]
    task = prompts[3]
    
    user_input = prompt.split("[SEP]")
    all_prompt = role + staff + task + examples + "Now that you have studdied the OPORD exames, you will create an OPORD one paragraph at a time."
    paragraphs = []
    topics = ["Orientation", "Situation", "Mission", "Execution", "Administration", "Logistics", "Command and Signal"]
    
    i = 0
    for t in topics:
        p = f"{all_prompt} Write the {t} parapgrah using the following subject: {user_input[i]}"
        i += 1
        
        model_inputs = tokenizer(p, return_tensors="pt").to(model.device)
        generated_ids = model.generate(**model_inputs, do_sample=True, max_new_tokens=1000, eos_token_id=tokenizer.eos_token_id)
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0][len(prompt):]
        paragraphs.append(response)
    
    response = "\n".join(paragraphs)
    save_response(response, " ".join(user_input), model)
    
    return response

def find_most_rel(query: str, index):
    """Returns the indices of the most related documents based on the user's query

    :param query: The user's query
    :type query: str
    :param index: The FAISS index of all of the corrosponding documents
    :type index: file
    :return: A list of the top k indices
    :rtype: list
    """
    query_embed = gen_embeds(query).cpu().detach().numpy().flatten().reshape(1, -1)
    faiss.normalize_L2(query_embed)
    _, top_k_indices = index.search(query_embed, 2)
    return top_k_indices[0]

def load_examples(type: str, prompt: str) -> str:
    """Returns real life examples of the requested document type.

    :param type: The document type
    :type type: str
    :param prompt: The prompt the user entered
    :type prompt: str
    :param prompt: The prompt the user entered
    :type prompt: str
    :return: A string of all of the examples concatenated together
    :rtype: str
    """
    # load in examples for few shot prompting
    examples = "Read the following examples very carefully. Your response must follow the same formatting as these examples.\n"

    data_path = "./data"

    paths = []

    # get paths to all example files
    for root, dirs, fnames in os.walk(data_path):
        if type in root:
            for f in fnames:
                if ".faiss" in f:
                    index = faiss.read_index(os.path.join(root, f))
                elif "pages" not in f:
                    paths.append(os.path.join(root, f))
                else:
                    continue
                    

    top_k_indices = find_most_rel(prompt, index)
    
    for k in top_k_indices:
        p = paths[k]
        if ".docx" in p:
            doc = Document(p)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n\n"
            
            examples += f"Example\n{text}\n\n"
        else:
            with open(paths[k], 'r') as f:
                examples += f"Example:\n{f.read()}\n\n"

    # if args.verbose:
    #     print(f"---------- EXAMPLES SELECTED FOR RAG ----------\n{examples}")
    #     print("---------- END EXAMPLES ----------")

    return examples

def save_response(response: str, prompt: str, model_name: str, model: str):
    """Writes the response and information about how it was generated to the disk.

    :param response: The document generated by the LLM
    :type response: str
    :param prompt: The prompt given by the user to the LLM to generate the document
    :type prompt: str
    :param model_name: The LLM model used to generate the document
    :type model_name: str
    :param model: The model object
    :type model: str
    """    
    # save response to file
    fname = datetime.now().strftime("%d-%b-%Y_%H:%M:%S")
    path = f"output/{fname}.txt"
    with open(path, 'w') as file:
        file.write(f"---------- RESPONSE ----------\n{response}\n\n")
        file.write(f"---------- PROMPT ----------\n{prompt}\n\n")
        file.write(f"---------- MODEL ----------\n{model_name}\n{model}")

def select_model(num: int) -> str:
    """Translates between the numeric representation of a model to the full string of its name.

    :param num: The model number selected from the menu
    :type num: int
    :return: The full string of the model name to fetch from the Hugging Face hub
    :rtype: str
    """    
    model = ""
    
    match num:
        case 1:
            model = "meta-llama/Llama-3.2-1B-Instruct"
        case 2:
            model = "meta-llama/Llama-3.2-3B-Instruct"
        case 3:
            model = "meta-llama/Llama-3.1-8B-Instruct"
        case _:
            model = "meta-llama/Llama-3.2-3B-Instruct"

    return model

def select_doc(num: int) -> str:
    """Translates between the numeric representation of a document type and its full name.

    :param num: The document number selected from the menu
    :type num: int
    :return: The full string of the document type to generate and fetch examples
    :rtype: str
    """
    type = ""
    
    match num:
        case 1:
            type = "NAVADMIN"
        case 2:
            type = "MARADMIN"
        case 3:
            type = "OpOrd"
        case 4:
            type = "RTW"
        case _:
            type = "NAVADMIN"

    return type

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates military documents using an LLM based on input from the user.")
    parser.add_argument("-k", "--top-k", type=int, help="Specify the number of related documents to identify for context when creating the new document, default is 3.", default=3)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()
    
    
    while True:
        try:
            # model to select model you want to load
            select = int(input("Select the Llama model you would like to run\n1) Llama 3.2 1B Instruct\n2) Llama 3.2 3B Instruct\n3) Llama 3.1 8B Instruct\n4) Exit\n> "))
            
            if select < 1 or select > 4:
                print("ERROR! you did not select a correct model option.")
                continue
            elif select == 4:
                print("Exiting...")
                quit()
    
            try:
                # get document type from user
                doc = int(input("Select document to generate\n1) Naval Message (NAVADMIN)\n2) USMC Message (MARADMIN)\n3) USMC OpOrd\n4) Road to War\n> "))
    
                if doc < 1 or doc > 4:
                    print("ERROR! You did not select a correct document options.")
                    continue
    
                user_query = input("Input> ")
                user_query = "Request: " + user_query

                # call document generator function
                doc = gen(select, doc, user_query)
            except ValueError:
                print("ERROR! Please only enter a number!")    
        except ValueError:
            print("ERROR! Please only enter a number!")    
