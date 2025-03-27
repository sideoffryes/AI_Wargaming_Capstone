# AI Wargaming: GenAI in Support of Wargaming Modernization

## USNA Demo Link

A live version of the project can be found [here](http://lnx1073302govt:5000).

**This link only works while on the USNA Intranet.**

## Description

Creating believable, realistic, and immersive scenarios in support of wargaming objectives
requires significant time and subject matter expertise. This capstone project proposes developing a
software system that leverages Large Language Models (LLMs) to automate the creation of critical wargaming
artifacts, such as "Road to War" briefs, concepts of operations, intelligence summaries, operational plans,
and operations orders. By utilizing an LLM system capable of generating detailed, context-specific
scenarios and associated products, this project aims to greatly accelerate the wargaming process,
potentially enhance the quality of the generated outputs, and reduce the need for extensive human resources.
The project may explore LLM techniques such as Retrieval-Augmented Generation (RAG), fine-tuning, and
prompt engineering, while also developing a user-friendly interface and ensuring real-time adaptability
based on user feedback. The final product will serve as a proof of concept, demonstrating how LLMs can
be harnessed to enhance and expedite the wargaming process.

## Installation

# Installation Instructions

1. Clone the project.

```console
$ git clone https://github.com/sideoffryes/AI_Wargaming_Capstone.git
```

2. Ensure that [Python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) are installed on your system.

3. Use the provided bash setup script (setup.sh) to create a virtual environment and install the necessary packages. You will be given several prompts throughout the process. During the process, you will be asked to provide a token to access Hugging Face. If you are not familiar with Hugging Face and access tokens, follow these instructions:

    1. Visit the page for the model on Hugging Face. For example, [Llama-3.2 (1B)](https://huggingface.co/meta-llama/Llama-3.2-1B)
    2. Create a free account and login.
    3. Return to the Llama webpage (if not already there).
    4. You should see a Community License Agreement at the top. Click the "Expand to review" button:
    5. If you agree with the terms, fill out the form
    6. Check email later.

Once you have received access to the models, visit your [tokens page](https://huggingface.co/settings/tokens) and click "Create new token". Choose the "Read" token type at the very top. Then click "Create token". Copy the generated string and paste when prompted during the setup process.

If you need to re-login at any point in the future, you can do so with the following command:

```console
$ (.venv) $ huggingface-cli login
```

The full setup script can be run with the following once you are set up with Hugging Face:

```console
$ ./setup.sh
```

4. If you did not choose to run the server at the end of the setup process, activate the newly-created virtual environment.

```console
$ source .venv/bin/activate
(.venv) $
```

6. The web server can be creating be entering the *capstone* directory and running the app.py script.

```console
(.venv) $ cd capstone
(.venv) $ python3 app.py
```

The IP addresses at which the server can be reached will be printed out to the terminal when the server is created.

7. If you did not choose to compile the documentation, it can be generated by entering the docs directory and compiling the HTML and/or the latex PDF version.

```console
(.venv) $ cd docs
(.venv) $ make html
```

```console
(.venv) $ cd docs
(.venv) $ make latexpdf
```

```console
(.venv) $ cd docs
(.venv) $ make html latexpdf
```

**IMPORTANT** You *must* generate the embeddings of the source documents before you attempt to generate any new documents using faissSetup.py. The NAVADMINS and MARADMINS must also be downloaded from the internet using the dataDownload.sh script.

```console
(.venv) $ ./dataDownload.sh
(.venv) $ cd capstone
(.venv) $ python3 faissSetup.py -d all
```

The -d option allows you to specify which embeddings to generate if you would only like to be able to generate a particular subset of documents. Run *python3 faissSetup.py -h* for a list of options.

A pre-compiled PDF version of the documentation can be found [here](./docs/build/latex/aiwargaming.pdf).

## Group Members

[Peter Asjes](mailto:m250228@usna.edu)

[William Robinson](mailto:m255334@usna.edu)

[Henry Frye](mailto:m251854@usna.edu)

[Caleb Koutrakos](mailto:m253300@usna.edu)

[Robert Ziman](mailto:m257074@usna.edu)

## POC

[LtCol Scotty Black](mailto:scotty.black@nps.edu )

## Poster

![Capstone Poster](./proposal/USNA%20Capstone%20Posterv2.png)
