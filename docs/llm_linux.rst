####################
Running LLM on Linux
####################

This page showcases an example of running LLM on RyzenAI NPU

- Open a Linux terminal and create a new folder

.. code-block:: bash

  mkdir run_llm
  cd run_llm

- You can choose any prequantized and postprocessed ready-to-run Model from `Hugging Face collection of NPU models <https://huggingface.co/collections/amd/ryzen-ai-16-npu-llm>`_
- We are using "Phi-3.5-mini-instruct-onnx-ryzenai-npu" for reference
.. code-block::

  # Make sure git-lfs is installed (https://git-lfs.com)
  git lfs install
  git clone https://huggingface.co/amd/Phi-3.5-mini-instruct-onnx-ryzenai-npu

- You can search for RYZEN_AI_INSTALLATION_PATH

.. code-block:: bash

  echo $RYZEN_AI_INSTALLATION_PATH
  <USER-PATH>/ryzen_ai-1.6.0/venv

- Collecting the necessary files to get in current working directory

.. code-block:: bash

  # Navigate to <USER-PATH>/ryzen_ai-1.6.0 and you will find a tar file "npu-llm.tar.gz" in the subdirectory
  cp <USER-PATH>/ryzen_ai-1.6.0/npu-llm.tar.gz .

  # unzip your file
  tar -xvzf npu-llm.tar.gz

  # Navigate to <USER-PATH>/ryzen_ai-1.6.0/venv path and you will find a "deployment" folder
  cp -r <USER-PATH>/ryzen_ai-1.6.0/venv/deployment .

                                    
- Your current working directory should have below files

.. code-block::

  deployment   npu-llm   npu-llm.tar.gz   Phi-3.5-mini-instruct-onnx-ryzenai-npu

- We have to update few files under Phi-3.5 Model to make it work for Linux environment 

.. code-block:: bash

  1) vim Phi-3.5-mini-instruct-onnx-ryzenai-npu/genai_config.json

      # Update line 8 to search for correct filename:
      "custom_ops_library": "deployment/lib/libonnx_custom_ops.so"
    
      # Add a flag under line 11 as shown below:
      "config_entries": {
          "hybrid_dbg_use_aie_rope": "0",

  2) vim Phi-3.5-mini-instruct-onnx-ryzenai-npu/.cache/MatMulNBits_2_0_meta.json 

      # We have to update Model Json file to port originally in Windows("\\") to now Linux("/") environment.
      - Windows flow - "file_name": ".cache\\MatMulNBits_2_0_0.const"
      - Linux flow   - "file_name": ".cache//MatMulNBits_2_0_0.const"
    
      # Helper script
       import json
    
       with open('Phi-3.5-mini-instruct-onnx-ryzenai-npu/.cache/MatMulNBits_2_0_meta.json','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if '.cache' in lines[i]:
                lines[i] = lines[i].replace('\\','/')
    
       with open('Phi-3.5-mini-instruct-onnx-ryzenai-npu/.cache/MatMulNBits_2_0_meta.json','w') as f:
         f.writelines(lines)

  
  
- Lastly, we need to add our directories for LD_LIBRARY_PATH

.. code-block:: bash

  export LD_LIBRARY_PATH=deployment/lib:$LD_LIBRARY_PATH

- We can now run our Model with command below:

.. code-block:: bash

  ./npu-llm/model_benchmark -i Phi-3.5-mini-instruct-onnx-ryzenai-npu/ -l 128 -p Phi-3.5-mini-instruct-onnx-ryzenai-npu/prompts.txt 

  # You can enable "-v" flag if you want verbose output


***************
Expected output
***************

.. code-block:: bash

  -----------------------------
  Prompt Number of Tokens: 128
  
  Batch size: 1, prompt tokens: 128, tokens to generate: 128
  Prompt processing (time to first token):
    	avg (us):       454882
    	avg (tokens/s): 281.392
    	p50 (us):       451257
    	stddev (us):    9252.73
    	n:              5 * 128 token(s)
  Token generation:
    	avg (us):       85176.2
    	avg (tokens/s): 11.7404
    	p50 (us):       84551.5
    	stddev (us):    7214.58
    	n:              635 * 1 token(s)
  Token sampling:
    	avg (us):       29.5788
    	avg (tokens/s): 33808
    	p50 (us):       28.052
    	stddev (us):    7.20914
    	n:              5 * 1 token(s)
  E2E generation (entire generation loop):
    	avg (ms):       11272.6
    	p50 (ms):       11284.3
    	stddev (ms):    42.6588
    	n:              5
  Peak CPU utilization (%): 19.5
  Avg CPU utilization (%): 1.7782
  ------------------
  Model create time (ms): 1549
  Peak working set size (megabytes) after initialization: 3051
  Peak working set size (megabytes): 6413

  Total runtime (ms): 70283
 


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

- Model Generate

  Generate the final model for NPU execution mode. Recommended to create a new output_dir folder 

  .. code-block:: bash

    model_generate --npu <output_dir> <quantized_model_path> --optimize decode

- Expected Output

  .. code-block:: bash

    NPU optimize decode model generated successfully.
    

===============
**Known Issues**
===============

1. Current release does not support these models

   - AMD-OLMo-1B-SFT-DPO, Llama-3.2-3B, Llama-3.2-3B-Instruct, Phi-4-mini-instruct, Phi-4-mini-reasoning

2. Here are list of models with known accuracy issue

   - chatglm3-6b, Meta-Llama-3.1-8B-Instruct, Mistral-7B-Instruct-v0.2, Mistral-7B-Instruct-v0.3
   - Qwen-2.5_1.5B_Instruct, Qwen2.5_3B_Instruct, Qwen2.5-7B-Instruct, Qwen2.5-Coder-1.5B-Instruct, Qwen2.5-Coder-7B-Instruct

