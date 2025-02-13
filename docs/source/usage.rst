Usage
=====

Installation
------------

Download the Code
^^^^^^^^^^^^^^^^^

The code for this project can be downloaded via `GitHub <https://github.com/sideoffryes/AI_Wargaming_Capstone/tree/main>`_.

.. code-block:: console

    $ git clone https://github.com/sideoffryes/AI_Wargaming_Capstone.git

Conda and Python Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use this project, the are several prerequisites that are necessary. The easiest way to manage these dependencies is using Conda.

If you do not have Conda already, `download and install a release <https://docs.anaconda.com/miniconda/install/>`_ for your OS.

All of the required python packages can be easily installed via the provided configuration files. There are separate files for GPU and CPU dependencies.

CPU
+++
.. code-block:: console

    (base) $ conda env create -f environment_cpu.yml

GPU
+++
.. code-block:: console

    (base) $ conda env create -f environment_gpu.yml

Hugging Face
^^^^^^^^^^^^

The project accesses the Llama 3.1, 3.2, and 3.3 families from Meta via Hugging Face. Running this project requires a Hugging Face account and access to those families.

1. Visit the page for the model on Hugging Face. For example, `Llama-3.2 (1B) <https://huggingface.co/meta-llama/Llama-3.2-1B>`_
2. Create a free account and login.
3. Return to the Llama webpage (if not already there).
4. You should see a Community License Agreement at the top. Click the "Expand to review" button:
5. If you agree with the terms, fill out the form
6. Check email later.

Once you have received access to the models, visit your `tokens page <https://huggingface.co/settings/tokens>`_ and click "Create new token". Choose the "Read" token type at the very top. Then click "Create token". Copy the generated string.

In the terminal, run the following command and paste in your access token when prompted:

.. code-block:: console

    (base) $ huggingface-cli login

Running the Project
-------------------

Before attempting to run any of the scripts, make sure that you have the correct Conda environment activated.

.. code-block:: console

    (base) $ conda activate capstone_gpu

All of the code that runs the webserver and actually generated the documents can be found inside of the *capstone* directory. *app.py* is the webserver and *docgen.py* is the script that accesses the LLM to generate documents. Running the entire project can be accomplished with the following:

.. code-block:: console
    
    (capstone_gpu) $ cd capstone
    (capstone_gpu) $ python3 app.py

The webserver can be reached from your browser by using one of the ip addresses printed out in the terminal when the server is created.

Interacting with the Webserver in the Browser
---------------------------------------------

The form presented to you when the website is first loaded can be used to generate a document. Use the *selection options* dropdown menu to select the type of document that you would like to create. You can specify your requirements and any additional specifications in the *additional parameters* textbox.

Depending on the size of the model used to generate the document, the server may load for a few minutes before the final output is produced.

Generating the Docs
-------------------

The repository is shipped with a precompiled PDF version of the documentation for the entire project for both users and developers.

The HTML documentation that can be viewed from the browser when running the webserver can be created by cding into the docs directory and using the make file.

.. code-block:: console

    (capstone_gpu) $ cd docs
    (capstone_gpu) $ make html

The generated documentation will appear in the docs/build/html directory.