.. Heading guidelines
..     # with overline, for parts
..     * with overline, for chapters
..     =, for sections
..     -, for subsections
..     ^, for subsubsections
..     “, for paragraphs

#####################
High-Level Python SDK
#####################

A Python environment offers flexibility for experimenting with LLMs, profiling them, and integrating them into Python applications. We use the `Lemonade SDK <https://github.com/lemonade-sdk/lemonade>`_ to get up and running quickly.

To get started, follow these instructions.

***************************
System-level pre-requisites
***************************

You only need to do this once per computer:

1. Make sure your system has the recommended Ryzen AI driver installed as described in :ref:`install-driver`.
2. Download and install `Miniconda for Windows <https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe>`_ or `Miniforge for Windows <https://github.com/conda-forge/miniforge/releases/download/25.3.0-1/Miniforge3-25.3.0-1-Windows-x86_64.exe>`.
3. Launch a terminal and call ``conda init``.


*****************
Environment Setup
*****************

To create and set up an environment, run these commands in your terminal:

.. code-block:: bash

    conda create -n ryzenai-llm python=3.10
    conda activate ryzenai-llm
    pip install lemonade-sdk[dev,oga-ryzenai] --extra-index-url=https://pypi.amd.com/simple

****************
Validation Tools
****************

Now that you have completed installation, you can try prompting an LLM like this (where ``PROMPT`` is any prompt you like).

Run this command in a terminal that has your environment activated:

.. code-block:: bash

    lemonade -i amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid oga-load --device hybrid --dtype int4 llm-prompt --max-new-tokens 64 -p PROMPT

Each example linked in the :ref:`featured-llms` table also has `example commands <https://github.com/amd/RyzenAI-SW/blob/main/example/llm/lemonade/hybrid/Llama_3_2_1B_Instruct.md#validation>`_ for validating the speed and accuracy of each model.

**********
Python API
**********
You can also run this code to try out the high-level Lemonade API in a Python script:

.. code-block:: python

  from lemonade.api import from_pretrained

  model, tokenizer = from_pretrained(
      "amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid", recipe="oga-hybrid"
  )

  input_ids = tokenizer("This is my prompt", return_tensors="pt").input_ids
  response = model.generate(input_ids, max_new_tokens=30)

  print(tokenizer.decode(response[0]))


**********
Next Steps
**********

From here, you can check out the Jupyter Notebook that provides an end-to-end validation of OGA hybrid and NPU-only execution. To run the notebook, visit the `Lemonade Tools Tutorial <https://github.com/lemonade-sdk/lemonade/blob/main/examples/notebooks/lemonade_model_validation.ipynb>`_.


..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
