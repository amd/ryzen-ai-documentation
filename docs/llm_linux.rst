####################
Running LLM on Linux
####################

This page showcase an example of running LLM on RyzenAI NPU

- Open a Linux terminal and create a new folder

.. code-block:: bash

  mkdir run_llm
  cd run_llm

- You can choose any Model from `Hugging Face collection of NPU models <https://huggingface.co/collections/amd/ryzenai-15-llm-npu-models-6859846d7c13f81298990db0>`_
- We are using "Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix" for reference
.. code-block::

  # Make sure git-lfs is installed (https://git-lfs.com)
  git lfs install
  git clone https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix

- You can search for RYZEN_AI_INSTALLATION_PATH

.. code-block::

  echo $RYZEN_AI_INSTALLATION_PATH
  <USER-PATH>/ryzen_ai-1.5.0/venv

- Navigate to Ryzen_ai-1.5.0 installation path and you will find a tar file "npu-llm.tar.gz" in the subdirectory

.. code-block::

  cp <USER-PATH>/ryzen_ai-1.5.0/npu-llm.tar.gz .

  # unzip your file
  tar -xvzf npu-llm.tar.gz


- Navigate to Ryzen_ai-1.5.0 virtual environment installation path and you will find a folder named "deployment" in the subdirectory

.. code-block:: bash

  cp <USER-PATH>/ryzen_ai-1.5.0/venv/deployment .

- Your current working directory should have below files

.. code-block::

  deployment  npu-llm  npu-llm.tar.gz  Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix

- We have to update a file under Phi-3.5 Model 

.. code-block::

  vim Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix/genai_config.json

  # update line 8 to search for correct filename:
  "custom_ops_library": "deployment/libonnxruntime_vitis_ai_custom_ops.so"

  
- Lastly, we need to add our directories for LD_LIBRARY_PATH

.. code-block::

  export LD_LIBRARY_PATH=deployment:$LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=npu_llm/lib:$LD_LIBRARY_PATH

- We can now run our Model with command below:

.. code-block::

  ./npu-llm/model_benchmark -i Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix/ -l 128 -p Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix/prompts.txt 


***************
Expected output
***************

.. code-block::

  I20250722 16:02:36.183243 23966 vitisai_compile_model.cpp:1157] Vitis AI EP Load ONNX Model Success
  I20250722 16:02:36.183279 23966 vitisai_compile_model.cpp:1158] Graph Input Node Name/Shape (66)
  I20250722 16:02:36.183287 23966 vitisai_compile_model.cpp:1162] 	 input_ids : [-1x-1]
  I20250722 16:02:36.183293 23966 vitisai_compile_model.cpp:1162] 	 attention_mask : [-1x-1]
  I20250722 16:02:36.183297 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.0.key : [-1x32x-1x96]
  I20250722 16:02:36.183305 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.0.value : [-1x32x-1x96]
  I20250722 16:02:36.183308 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.1.key : [-1x32x-1x96]
  I20250722 16:02:36.183315 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.1.value : [-1x32x-1x96]
  I20250722 16:02:36.183318 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.2.key : [-1x32x-1x96]
  I20250722 16:02:36.183322 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.2.value : [-1x32x-1x96]
  I20250722 16:02:36.183327 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.3.key : [-1x32x-1x96]
  I20250722 16:02:36.183332 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.3.value : [-1x32x-1x96]
  I20250722 16:02:36.183336 23966 vitisai_compile_model.cpp:1162] 	 past_key_values.4.key : [-1x32x-1x96]









