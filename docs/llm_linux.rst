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
  sudo apt install git-lfs
  git lfs install
  git clone https://huggingface.co/amd/Phi-3.5-mini-instruct-onnx-ryzenai-npu

- Search for RYZEN_AI_INSTALLATION_PATH

.. code-block:: bash

  # Activate the virtual environment created in Linux Installation step
  source <TARGET-PATH>/venv/bin/activate

  echo $RYZEN_AI_INSTALLATION_PATH

- Collecting the necessary files to get in current working directory

.. code-block:: bash

  - Deployment folder - This has necessary libraries to run LLM Model
      # Navigate to <TARGET-PATH>/venv and copy the "deployment" folder
      cp -r <TARGET-PATH>/venv/deployment .

  - Model Benchmark Script 
      # Navigate to <TARGET-PATH>/venv/LLM/examples/ and copy "model_benchmark" file.
      cp <TARGET-PATH>/venv/LLM/examples/model_benchmark .

  - Prompt file - Input to your LLM Model
      # Navigate to <TARGET-PATH>/venv/LLM/examples/ and copy "amd_genai_prompt.txt" file.
      cp <TARGET-PATH>/venv/LLM/examples/amd_genai_prompt.txt .

                                    
- Current working directory should have below files

.. code-block::

  amd_genai_prompt.txt   deployment   model_benchmark   Phi-3.5-mini-instruct-onnx-ryzenai-npu

- Create a new file for XRT Drivers named "xrt.ini"

.. code-block:: bash

      - vi xrt.ini            (Creates a new file)
    
      - Add below lines to the file and save it
          [Debug]
          num_heap_pages = 8  

      - Set XRT_INI_PATH to point to this file
          export XRT_INI_PATH=$PWD/xrt.ini
  
- Lastly, add directories for LD_LIBRARY_PATH

.. code-block:: bash

  export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=deployment/lib:$LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=$PWD/deployment/lib/libonnxruntime_providers_ryzenai.so:$LD_LIBRARY_PATH
  

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
        avg (us):       416591
        avg (tokens/s): 307.256
        p50 (us):       413180
        stddev (us):    7532.87
        n:              5 * 128 token(s)
 Token generation:
        avg (us):       90500.9
        avg (tokens/s): 11.0496
        p50 (us):       89802.8
        stddev (us):    7364.33
        n:              635 * 1 token(s)
 Token sampling:
        avg (us):       30.0704
        avg (tokens/s): 33255.3
        p50 (us):       27.752
        stddev (us):    5.21835
        n:              5 * 1 token(s)
 E2E generation (entire generation loop):
        avg (ms):       11910.3
        p50 (ms):       11898.2
        stddev (ms):    22.1976
        n:              5
 Peak working set size (bytes): 6483783680


 


*******************
Preparing OGA Model
*******************

Currently Linux supports NPU only flow. Read more on Model Generation by visiting :doc:`Preparing OGA Models <oga_model_prepare>`
  


