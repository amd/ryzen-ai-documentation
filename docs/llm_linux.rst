####################
Running LLM on Linux
####################

This page showcases an example of running LLM on RyzenAI NPU

- Open a Linux terminal and create a new folder

.. code-block:: bash

  mkdir run_llm
  cd run_llm

- Choose any prequantized and postprocessed ready-to-run Model from `Hugging Face collection of NPU models <https://huggingface.co/collections/amd/ryzen-ai-16-npu-llm>`_
- For this flow, "Phi-3.5-mini-instruct-onnx-ryzenai-npu" is chosen for reference
.. code-block::

  # Make sure git-lfs is installed (https://git-lfs.com)
  git lfs install
  git clone https://huggingface.co/amd/Phi-3.5-mini-instruct-onnx-ryzenai-npu

- Search for RYZEN_AI_INSTALLATION_PATH

.. code-block:: bash

  echo $RYZEN_AI_INSTALLATION_PATH
  <TARGET-PATH>/ryzen_ai-1.6.0/venv

  # Activate the virtual environment
  source <TARGET-PATH>/ryzen_ai-1.6.0/venv/bin/activate

- Collecting the necessary files to get in current working directory

.. code-block:: bash

  - Deployment folder - This has necessary libraries to run LLM Model
      # Navigate to <TARGET-PATH>/ryzen_ai-1.6.0/venv and copy the "deployment" folder
      cp -r <TARGET-PATH>/ryzen_ai-1.6.0/venv/deployment .

  - Model Benchmark Script 
      # Navigate to <TARGET-PATH>/ryzen_ai-1.6.0/venv/LLM/examples/ and copy "model_benchmark" file.
      cp <TARGET-PATH>/ryzen_ai-1.6.0/venv/LLM/examples/model_benchmark .

  - Prompt file - Input to your LLM Model
      # Navigate to <TARGET-PATH>/ryzen_ai-1.6.0/venv/LLM/examples/ and copy "amd_genai_prompt.txt" file.
      cp <TARGET-PATH>/ryzen_ai-1.6.0/venv/LLM/examples/amd_genai_prompt.txt .

                                    
- Current working directory should have below files

.. code-block::

  deployment   model_benchmark   amd_genai_prompt.txt   Phi-3.5-mini-instruct-onnx-ryzenai-npu

- Two files under Phi-3.5 Model have to be updated to make it work for Linux environment 

.. code-block:: bash

  1) Edit genai_config.json file under Model folder: 

      - "custom_ops_library": "deployment/lib/libonnx_custom_ops.so"    (line 8)  
    
      - "config_entries": {
          "hybrid_dbg_use_aie_rope": "0",                               (line 11 - Add flag under config_entries)


  2) Edit .cache/MatMulNBits_2_0_meta.json file under Model folder:

      # Python utility script helps convert Windows-style paths in "MatMulNBits_2_0_meta.json" to Linux-style paths

      # Python utility script
       import json
    
       with open('Phi-3.5-mini-instruct-onnx-ryzenai-npu/.cache/MatMulNBits_2_0_meta.json','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if '.cache' in lines[i]:
                lines[i] = lines[i].replace('\\','/')
    
       with open('Phi-3.5-mini-instruct-onnx-ryzenai-npu/.cache/MatMulNBits_2_0_meta.json','w') as f:
         f.writelines(lines)

  
- Lastly, add directories for LD_LIBRARY_PATH

.. code-block:: bash

  export LD_LIBRARY_PATH=deployment/lib:$LD_LIBRARY_PATH

- We can now run our Model with command below:

.. code-block:: bash

  ./model_benchmark -i Phi-3.5-mini-instruct-onnx-ryzenai-npu/ -l 128 -f amd_genai_prompt.txt

  # Enable "-v" flag for verbose output


***************
Expected output
***************

.. code-block:: bash

 -----------------------------
 Prompt Number of Tokens: 128
  
 Batch size: 1, prompt tokens: 128, tokens to generate: 128
 Prompt processing (time to first token):
    avg (us):       442251
    avg (tokens/s): 289.428
    p50 (us):       442583
    stddev (us):    4901.59
    n:              5 * 128 token(s)
 Token generation:
    avg (us):       85353.7
    avg (tokens/s): 11.716
    p50 (us):       84689.3
    stddev (us):    7012.99
    n:              635 * 1 token(s)
 Token sampling:
    avg (us):       27.4852
    avg (tokens/s): 36383.2
    p50 (us):       27.652
    stddev (us):    0.928063
    n:              5 * 1 token(s)
  E2E generation (entire generation loop):
    avg (ms):       11282.4
    p50 (ms):       11275.4
    stddev (ms):    14.2974
    n:              5
 Peak working set size (bytes): 6736375808

 


*******************
Preparing OGA Model
*******************

Preparing OGA Model is a two-step process

==================
Model Quantization
==================

- Follow Model Quantization steps described here :doc:`oga_model_prepare`

===============
Postprocessing
===============

-  Model Quantization step produces Pytorch quantized model. 
-  Model_generate script initially converts Pytorch quantized model to Onnx format and subsequently postprocesses to run for NPU Execution mode. 

.. code-block:: bash

  pip install onnx-ir 

  model_generate --npu <output_dir> <quantized_model_path> --optimize decode

- Expected Output

.. code-block:: bash

  NPU optimize decode model generated successfully.
  


