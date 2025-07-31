####################
Running LLM on Linux
####################

This page showcases an example of running LLM on RyzenAI NPU

- Open a Linux terminal and create a new folder

.. code-block:: bash

  mkdir run_llm
  cd run_llm

- You can choose any prequantized and postprocessed ready-to-run Model from `Hugging Face collection of NPU models <https://huggingface.co/collections/amd/ryzenai-15-llm-npu-models-6859846d7c13f81298990db0>`_
- We are using "Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix" for reference
.. code-block::

  # Make sure git-lfs is installed (https://git-lfs.com)
  git lfs install
  git clone https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix

- You can search for RYZEN_AI_INSTALLATION_PATH

.. code-block:: bash

  echo $RYZEN_AI_INSTALLATION_PATH
  <USER-PATH>/ryzen_ai-1.5.0/venv

- Navigate to Ryzen_ai-1.5.0 installation path and you will find a tar file "npu-llm.tar.gz" in the subdirectory

.. code-block:: bash

  cp <USER-PATH>/ryzen_ai-1.5.0/npu-llm.tar.gz .

  # unzip your file
  tar -xvzf npu-llm.tar.gz

- Your current working directory should have below files

.. code-block::

  npu-llm  npu-llm.tar.gz  Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix

- We have to update a file under Phi-3.5 Model 

.. code-block:: bash

  vim Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix/genai_config.json

  # update line 8 to search for correct filename:
  "custom_ops_library": "npu-llm/lib/libonnxruntime_vitis_ai_custom_ops.so"

  
- Lastly, we need to add our directories for LD_LIBRARY_PATH

.. code-block:: bash

  export LD_LIBRARY_PATH=npu-llm/lib:$LD_LIBRARY_PATH

- We can now run our Model with command below:

.. code-block:: bash

  ./npu-llm/model_benchmark -i Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix/ -l 128 -p Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix/prompts.txt 


***************
Expected output
***************

.. code-block:: bash

  [Vitis AI EP] No. of Operators :   CPU    41 MATMULNBITS   195  SSMLP    32 
  [Vitis AI EP] No. of Subgraphs :MATMULNBITS    65  SSMLP    32 
  -----------------------------
  Prompt Number of Tokens: 128
  
  Batch size: 1, prompt tokens: 128, tokens to generate: 128
  Prompt processing (time to first token):
  	avg (us):       256407
  	avg (tokens/s): 499.207
  	p50 (us):       255675
  	stddev (us):    2978.1
  	n:              5 * 128 token(s)
  Token generation:
  	avg (us):       81849.6
  	avg (tokens/s): 12.2175
  	p50 (us):       81782.7
  	stddev (us):    3138.29
  	n:              635 * 1 token(s)
  Token sampling:
  	avg (us):       27.1502
  	avg (tokens/s): 36832.1
  	p50 (us):       27.25
  	stddev (us):    0.812347
  	n:              5 * 1 token(s)
  E2E generation (entire generation loop):
  	avg (ms):       10651.6
  	p50 (ms):       10665.2
  	stddev (ms):    28.0445
  	n:              5
  Peak CPU utilization (%): inf
  Avg CPU utilization (%): inf
  ----------------------------
  Model create time (ms): 3634
  Peak working set size (megabytes) after initialization: 4039
  Peak working set size (megabytes): 4172
  
  Total runtime (ms): 68011  


************
Model Cache
************
By default cache is stored under /tmp/<User-name>/vaip/.cache

  

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

- Download and install the Python wheel in Ryzen-AI Virtual Environment

  .. code-block:: bash

    # Activate your Virtual Environment
    source <TARGET-PATH>/venv/bin/activate
    pip install model-generate==1.5.0 --extra-index-url=https://pypi.amd.com/simple


- Model Generate

  - Generate the final model for NPU execution mode 

  .. code-block:: bash

    model_generate --npu <output_dir> <quantized_model_path>

- Expected Output

  .. code-block:: bash

    Generate completed successfully!
    NPU model generation completed successfully.
    

===============
**Known Issues**:
===============

1. The following models are not supported in this release due to known issues:

   - DeepSeek-R1-Distill-Qwen-7B, Qwen2.5-7B-Instruct, Qwen2-7B-Instruct

2. Some models in the `Hugging Face collection of NPU models <https://huggingface.co/collections/amd/ryzenai-15-llm-npu-models-6859846d7c13f81298990db0>`_ require regeneration (quantization and postprocessing) to run on Linux.


