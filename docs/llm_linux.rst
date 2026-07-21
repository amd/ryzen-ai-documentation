####################
Running LLM on Linux
####################

This page showcases an example of running LLM on RyzenAI NPU

- Open a Linux terminal and create a new folder

.. code-block:: bash

  mkdir run_llm
  cd run_llm

- Here is an Overview of all supported Models :doc:`List of Supported Models <llm_linux.rst>` 

- Choose any prequantized and postprocessed ready-to-run Model from Hugging Face collection of NPU models

.. parsed-literal::

    `Models with 4K Context length <https://huggingface.co/collections/amd/ryzen-ai-171-npu-4k>`_

    `Models with 16K Context length <https://huggingface.co/collections/amd/ryzen-ai-171-npu-16k>`_

- For this flow, "Phi-3.5-mini-instruct_rai_1.7.1_npu_4K" is chosen for reference
.. code-block::

  # Make sure git-lfs is installed (https://git-lfs.com)
  sudo apt install git-lfs
  git lfs install
  git clone https://huggingface.co/amd/Phi-3.5-mini-instruct_rai_1.7.1_npu_4K

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

  amd_genai_prompt.txt   deployment   model_benchmark   Phi-3.5-mini-instruct_rai_1.7.1_npu_4K

- Lastly, set required library path

.. code-block:: bash

  export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:deployment/lib:$LD_LIBRARY_PATH
  export RYZENAI_EP_PATH=$PWD/deployment/lib/libonnxruntime_providers_ryzenai.so
  source /opt/xilinx/xrt/setup.sh

- We can now run our Model with command below:

.. code-block:: bash

  ./model_benchmark -i Phi-3.5-mini-instruct_rai_1.7.1_npu_4K/ -l 128 

   -i - Path to the ONNX model directory to benchmark
   -l - Number of tokens in the generated prompt (Default: 16)
   
  # Use "./model_benchmark --help" to enable more options


***************
Expected output
***************

.. code-block:: bash

 -----------------------------
 Prompt Number of Tokens: 128
  
 Batch size: 1, prompt tokens: 128, tokens to generate: 128
 Prompt processing (time to first token):
        avg (us):       169860
        avg (tokens/s): 753.562
        p50 (us):       169022
        stddev (us):    6108.17
        n:              5 * 128 token(s)
 Token generation:
        avg (us):       20354.1
        avg (tokens/s): 49.1301
        p50 (us):       19964.9
        stddev (us):    4411.67
        n:              635 * 1 token(s)
 Token sampling:
        avg (us):       192.274
        avg (tokens/s): 5200.91
        p50 (us):       202.417
        stddev (us):    76.6932
        n:              5 * 1 token(s)
 E2E generation (entire generation loop):
        avg (ms):       2755.09
        p50 (ms):       2747.84
        stddev (ms):    14.0296
        n:              5
 Peak working set size (bytes): 3543330816


 


*******************
Preparing OGA Model
*******************

Model Generate is not supported in current release. Choose any prequantized and postprocessed ready-to-run Model from the provided list.
Read more on Windows specific Model Generation by visiting :doc:`Preparing OGA Models <oga_model_prepare>`


  


