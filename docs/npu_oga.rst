:orphan:

######################
OGA NPU Execution Mode
######################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. This documentation covers the NPU execution mode for LLMs, which utilizes only the NPU.  

**Note**: Refer to :doc:`hybrid_oga` for Hybrid NPU + GPU execution mode.


************************
Supported Configurations
************************

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.


************
Requirements
************
- Install NPU Drivers and RyzenAI MSI installer according to the instructions https://ryzenai.docs.amd.com/en/latest/inst.html. 
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads


********************
Pre-optimized Models
********************

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for NPU execution. These models can be found on Hugging Face in the following collection:

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
- https://huggingface.co/amd/DeepSeek-R1-Distill-Llama-8B-awq-g128-int4-asym-bf16-onnx-ryzen-strix  
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-1.5B-awq-g128-int4-asym-bf16-onnx-ryzen-strix 
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-7B-awq-g128-int4-asym-bf16-onnx-ryzen-strix   
- https://huggingface.co/amd/AMD-OLMo-1B-SFT-DPO-awq-g128-int4-asym-bf16-onnx-ryzen-strix

The steps for deploying the pre-optimized models using C++ and python are described in the following sections.

***************************
NPU Execution of OGA Models
***************************

Setup
=====

1. Install Ryzen AI 1.4 according to the instructions if not installed previously: https://ryzenai.docs.amd.com/en/latest/inst.html

2. Activate the Ryzen AI 1.4 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.4.0

NOTE: pre-built versions of the ``run_llm.exe`` and ``model_generate.exe`` executables are already available in the ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/exe`` folder. If you choose to use them directly, you can skip to step 5 and copy the executables to ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/libs``. Otherwise follow the steps below to build the applications from source. 

3. Open command prompt and navigate to the ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/cpp`` folder 

.. code-block::

  # Switch to cpp folder 
  cd %RYZEN_AI_INSTALLATION_PATH%/npu-llm/cpp

4. Compile 

.. code-block::
 
   cmake -G "Visual Studio 17 2022" -A x64 -S . -B build 
   cd build 
   cmake --build . --config Release 

**Note**: The executable created ``run_llm.exe`` and ``model_generate.exe`` can be found in ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm/cpp/build/Release`` folder 

 
5. Copy the executables ``run_llm.exe`` and ``model_generate.exe`` to the ``npu-llm/libs`` folder. The ``npu-llm/libs`` should contain both: ``run_llm.exe``, ``model_benchmark.exe`` along with the ``.dll`` files it contains. 
 
.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%\npu-llm
   xcopy .\cpp\build\Release\model_benchmark.exe .\libs 
   xcopy .\cpp\build\Release\run_llm.exe .\libs 


Download Models from HuggingFace
================================

1. Navigate to the ``npu-llm`` folder: 

.. code-block:: 
    
    cd %RYZEN_AI_INSTALLATION_PATH%\npu-llm

2. Download from Hugging Face the desired models (from the list of published models):

.. code-block:: 
    
     # Make sure you have git-lfs installed (https://git-lfs.com) 
     git lfs install  
     git clone <link to hf model> 

For example, for Llama-2-7b:

.. code-block:: 

     git lfs install  
     git clone https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix


Enabling Performance Mode (Optional)
====================================

To run the LLMs in the best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power`` and set the power mode to Best Performance.
- Execute the following commands in the terminal:

.. code-block::

   cd C:\Windows\System32\AMD
   xrt-smi configure --pmode performance



Run the Models using C++
========================

**Note**: Ensure the models are cloned in the ``%RYZEN_AI_INSTALLATION_PATH%/npu-llm`` folder.


The ``run_llm.exe`` program provides a simple interface to run LLMs. It supports the following command line options:: 

    -m: model path
    -f: prompt file
    -n: max new tokens
    -c: use chat template
    -t: input prompt token length
    -l: max length to be set in search options
    -h: help


Example usage:

.. code-block::

   .\libs\run_llm.exe -m .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -f .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -t "1024" -n 20 

|

The ``model_benchmark.exe`` program can be used to profile the execution of LLMs and report various metrics. It supports the following command line options:: 

    -i,--input_folder <path>
      Path to the ONNX model directory to benchmark, compatible with onnxruntime-genai.
    -l,--prompt_length <numbers separated by commas>
      List of number of tokens in the prompt to use.
    -p,--prompt_file <filename>
      Name of prompt file (txt) expected in the input model directory.
    -g,--generation_length <number>
      Number of tokens to generate. Default: 128
    -r,--repetitions <number>
      Number of times to repeat the benchmark. Default: 5
    -w,--warmup <number>
      Number of warmup runs before benchmarking. Default: 1
    -t,--cpu_util_time_interval <number in ms>
      Sampling time interval for peak cpu utilization calculation, in milliseconds. Default: 250
    -v,--verbose
      Show more informational output.
    -h,--help
      Show this help message and exit.


Example usage:

.. code-block::
   
   .\libs\model_benchmark.exe -i .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix -g 20 -p .\Llama-2-7b-hf-awq-g128-int4-asym-bf16-onnx-ryzen-strix\prompts.txt -l "2048,1024,512,256,128" 



Run the Models using Python
===========================

1. In the model directory, open the ``genai_config.json`` file located in the folder of the downloaded model. Update the value of the "custom_ops_library" key with the full path to the ``onnxruntime_vitis_ai_custom_ops.dll``, located in the ``%RYZEN_AI_INSTALLATION_PATH%\npu-llm\libs`` folder:  

.. code-block::
  
      "session_options": {
                ...
                "custom_ops_library": "C:\\Program Files\\RyzenAI\\1.4.0\\npu-llm\\libs\\onnxruntime_vitis_ai_custom_ops.dll",
                ...
      }

2. To run using the native OGA Python APIs, use the following commands. 

.. code-block::

   (ryzen-ai-1.4.0) cd %RYZEN_AI_INSTALLATION_PATH%/npu-llm
   

- To run any model other than chatglm: 

.. code-block:: 

     (ryzen-ai-1.4.0)python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\llama3\run_model.py" --model_dir <model folder>  

- To run chatglm: 

.. code-block:: 

     #chatglm needs transformers 4.44.0 
     (ryzen-ai-1.4.0)pip install transformers==4.44.0  
     (ryzen-ai-1.4.0)python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\chatglm\model-generate-chatglm3.py" -m <model folder>  

 
*******************************************
Preparing OGA Models for NPU-only Execution
*******************************************

To prepare the OGA model for NPU-only execution please refer :doc:`oga_model_prepare` 
