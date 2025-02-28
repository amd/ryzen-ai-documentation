:orphan:

######################
OGA NPU Execution Mode
######################

.. note::
   
   Support for LLMs is currently in the Early Access stage. Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.

Starting with version 1.3, the Ryzen AI Software includes support for deploying LLMs on Ryzen AI PCs using the ONNX Runtime generate() API (OGA). This documentation is for the NPU execution of LLMs when using the OGA API.

Supported Configurations
~~~~~~~~~~~~~~~~~~~~~~~~

The Ryzen AI OGA flow supports the following processors running Windows 11:

- Strix (STX): AMD Ryzen™ Ryzen AI 9 HX375, Ryzen AI 9 HX370, Ryzen AI 9 365

**Note**: Phoenix (PHX) and Hawk (HPT) processors are not supported.

Requirements
~~~~~~~~~~~~
- NPU Driver (version .237): Install according to the instructions https://ryzenai.docs.amd.com/en/latest/inst.html
- NPU LLM artifacts package: ``npu-llm-artifacts_1.3.0.zip`` from https://account.amd.com/en/member/ryzenai-sw-ea.html

Setting performance mode (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the LLMs in the best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power`` and set the power mode to Best Performance.
- Execute the following commands in the terminal:

.. code-block::

   cd C:\Windows\System32\AMD
   xrt-smi configure --pmode performance


Package Contents
~~~~~~~~~~~~~~~~

NPU LLM artifacts package contains the files required to build and run applications using the ONNX Runtime generate() API (OGA) to deploy LLMs on NPU. The list below describes which files are needed for the different use cases:

- C++ code to run LLM on NPU 

  - amd_oga/cpp/src/run_llm.cpp 
- Runtime DLL and lib files in ``amd_oga/libs``

  - onnxruntime.dll 
  - onnxruntime_providers_shared.dll 
  - onnxruntime_providers_vitisai.dll 
  - onnxruntime_vitisai_ep.dll 
  - onnxruntime_vitis_ai_custom_ops.dll 
  - onnxruntime-genai.dll 
  - dyn_dispatch_core.dll 
  - transaction.dll 
  - onnxruntime-genai.lib 
- NPU binary file 
  
  - amd_oga/bins/xclbin/stx/llama2_mladf_2x4x4_v1_gemmbfp16_silu_mul_mha_rms_rope.xclbin 
- Executables 
 
  - amd_oga/exe/run_llm.exe 
  - amd_oga/exe/model_benchmark.exe 
- Batch Files 

  - run.bat 
  - run_benchmark.bat 
- Python wheel files (Python 3.10) 

  - onnxruntime_genai-0.5.0.dev0-cp310-cp310-win_amd64.whl 
  - onnxruntime_vitisai-1.20.0-cp310-cp310-win_amd64.whl 
  - voe-1.3.1-cp310-cp310-win_amd64.whl 

Pre-optimized Models
~~~~~~~~~~~~~~~~~~~~

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for NPU execution. These models can be found on Hugging Face in the following collection:

https://huggingface.co/collections/amd/quark-awq-g128-int4-asym-bf16-onnx-npu-13-6759f510b8132db53e044aaf

- https://huggingface.co/amd/Phi-3-mini-4k-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.3-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Qwen1.5-7B-Chat-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/chatglm3-6b-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama2-7b-chat-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3-8B-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3.1-8B-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix
- https://huggingface.co/amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-bf16-onnx-ryzen-strix

The steps for deploying the pre-optimized models using C++ are described in the following sections.

NPU Execution of OGA Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build the Test Applications 
@@@@@@@@@@@@@@@@@@@@@@@@@@@

NOTE: pre-built versions of the ``run_llm.exe`` and ``model_generate.exe`` executables are already available in the ``amd_oga/exe`` folder. If you choose to use them directly, you can skip to step 3 and copy the executables to ``amd_oga/libs``. Otherwise follow the steps below to build the applications from source. 

1. Open command prompt and navigate to the ``amd_oga/cpp`` folder 

.. code-block::

  # Switch to cpp folder 
  cd amd_oga/cpp 

2. Compile 

.. code-block::
 
   cmake -G "Visual Studio 17 2022" -A x64 -S . -B build 
   cd build 
   cmake --build . --config Release 

**Note**: The executable created ``run_llm.exe`` and ``model_generate.exe`` can be found in ``amd_oga/cpp/build/Release`` folder 

 
3. Copy the executables ``run_llm.exe`` and ``model_generate.exe`` to the ``amd_oga/libs`` folder. The ``amd_oga/libs`` should contain both: ``run_llm.exe``, ``model_benchmark.exe`` along with the ``.dll`` files it contains. 
 
.. code-block::

   cd amd_oga 
   xcopy .\cpp\build\Release\model_benchmark.exe .\libs 
   xcopy .\cpp\build\Release\run_llm.exe .\libs 

Set the environment variables
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block::

   set DD_ROOT=./bins 
   set XLNX_ENABLE_CACHE=0 

Run the models
@@@@@@@@@@@@@@

**Note**: Ensure the models are cloned in the ``amd_oga`` folder.

Run using a batch file
**********************

The ``run.bat`` batch file located in the ``amd_oga`` directory contains commands for running multiple models. If you wish to run only a specific model, you can do so by uncommenting the corresponding command and commenting out others.  
 
For example, to run only Llama2-7b, ensure the line shown below is uncommented, and other commands are commented (preceded by REM). 

.. code-block::

   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -c -t "2048,1024,512,256,128" 

Run the models using run.bat: 

.. code-block::

   # Run the batch file 
   cd amd_oga 
   run.bat 

Run manually
************

To run the models using the ``run_llm.exe`` file 

.. code-block::

   cd amd_oga 
   # Help 
   .\libs\run_llm.exe -h 
 
   # To enter prompt through command prompt, and default max new tokens 
   .\libs\run_llm.exe -m <model_path> 

   # For example,  
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix 

   # To provide max new tokens value which is set to 32 by default 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens>  

   # For example, 
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 

   # To provide prompts through a prompt file 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens> -f <model_path>\<prompts.txt> 

   # For example:  
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt 

   # To use chat template 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens> -f <model_path>\<prompts.txt> -c 

   # For example:  
   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -c 

   # To specify prompt length 
   .\libs\run_llm.exe -m <model_path> -n <max_new_tokens> -f <model_path>\<prompts.txt> -t "list_prompt_lengths" 

   # For example,  

   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -n 20 -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -t "2048,1024,512,256,128" 

 
Run Benchmark
@@@@@@@@@@@@@

Run using a batch file
**********************

The ``run_benchmark.bat`` batch file located in the ``amd_oga`` directory contains commands for running multiple models. If you wish to run only a specific model, you can do so by uncommenting the corresponding command and commenting out others.  
 
For example, to run only Llama2-7b, ensure the line shown below is uncommented, and other commands are commented (preceded by REM). 

.. code-block::

    .\libs\model_benchmark.exe -i .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -g 20 -p .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -l "2048,1024,512,256,128" 

 
Run the models using run_benchmark.bat:  

.. code-block::

   # Run the batch file 
   cd amd_oga 
   run_benchmark.bat 

 
Run manually
************

To run the models using the ``model_benchmark.exe`` file 
 
.. code-block::

   cd amd_oga 
   # Help 
   .\libs\model_benchmark.exe -h 
   
   # Run with default settings 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" 
   
   # For example:  
   .\libs\model_benchmark.exe -i .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -p .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -l "2048,1024,512,256,128" 

   # To specify number of tokens to generate, default 128 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -g num_tokens 

   # For example:  
   .\libs\model_benchmark.exe -i .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -g 20 -p .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -l "2048,1024,512,256,128" 

   # To specify number of warmup iterations before benchmarking, default: 1 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -w num_warmup 

   # To specify number of times to repeat the benchmark, default: 5 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -r num_iterations 

   # To specify sampling time interval for peak cpu utilization calculation, in milliseconds. Default: 250 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> -l "list_of_prompt_lengths" -t time_in_milliseconds 

   # To show more informational output 
   .\libs\model_benchmark.exe -i <model_path> -p <model_path>\<prompts.txt> --verbose 

 
Preparing OGA Models for NPU-only Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To prepare the OGA model for NPU-only execution please refer :doc:`oga_model_prepare` 

