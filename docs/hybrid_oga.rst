############################
OnnxRuntime GenAI (OGA) Flow 
############################

Ryzen AI Software supports deploying LLMs on Ryzen AI PCs using the native ONNX Runtime Generate (OGA) C++ or Python API. The OGA API is the lowest-level API available for building LLM applications on a Ryzen AI PC. This documentation covers the Hybrid execution mode for LLMs, which utilizes both the NPU and GPU 

**Note**: Refer to :doc:`npu_oga` for NPU only execution mode.  

************************
Supported Configurations
************************

The Ryzen AI OGA flow supports Strix and Krackan Point processors. Phoenix (PHX) and Hawk (HPT) processors are not supported.


************
Requirements
************

- Install NPU Drivers and Ryzen AI MSI installer according to the :doc:`inst`
- Install GPU device driver: Ensure GPU device driver https://www.amd.com/en/support is installed 
- Install Git for Windows (needed to download models from HF): https://git-scm.com/downloads

********************
Pre-optimized Models
********************

AMD provides a set of pre-optimized LLMs ready to be deployed with Ryzen AI Software and the supporting runtime for hybrid execution. These models can be found on Hugging Face: 

- https://huggingface.co/amd/Phi-3-mini-4k-instruct-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.3-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Qwen1.5-7B-Chat-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/chatglm3-6b-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Llama-2-7b-hf-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Llama-3-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main 
- https://huggingface.co/amd/Llama-3.1-8B-awq-g128-int4-asym-fp16-onnx-hybrid/tree/main 
- https://huggingface.co/amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid 
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.1-hybrid 
- https://huggingface.co/amd/Mistral-7B-Instruct-v0.2-hybrid 
- https://huggingface.co/amd/Mistral-7B-v0.3-hybrid 
- https://huggingface.co/amd/Llama-3.1-8B-Instruct-hybrid 
- https://huggingface.co/amd/CodeLlama-7b-instruct-g128-hybrid 
- https://huggingface.co/amd/DeepSeek-R1-Distill-Llama-8B-awq-asym-uint4-g128-lmhead-onnx-hybrid 
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-1.5B-awq-asym-uint4-g128-lmhead-onnx-hybrid
- https://huggingface.co/amd/DeepSeek-R1-Distill-Qwen-7B-awq-asym-uint4-g128-lmhead-onnx-hybrid
- https://huggingface.co/amd/AMD-OLMo-1B-SFT-DPO-hybrid
- https://huggingface.co/amd/Qwen2-7B-awq-uint4-asym-g128-lmhead-fp16-onnx-hybrid
- https://huggingface.co/amd/Qwen2-1.5B-awq-uint4-asym-global-g128-lmhead-g32-fp16-onnx-hybrid
- https://huggingface.co/amd/gemma-2-2b-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
- https://huggingface.co/amd/Qwen2.5-1.5B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
- https://huggingface.co/amd/Qwen2.5-3B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
- https://huggingface.co/amd/Qwen2.5-7B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid

The steps for deploying the pre-optimized models using Python or C++ are described in the following sections.

******************************
Hybrid Execution of OGA Models
******************************

Setup
=====

Activate the Ryzen AI 1.4.1 Conda environment:

.. code-block:: 
    
    conda activate ryzen-ai-1.4.1

Copy the required files in a local folder to run the LLMs from:

.. code-block::
  
     mkdir hybrid_run
     cd hybrid_run
     xcopy /Y /E "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\onnxruntime_genai\benchmark" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\amd_genai_prompt.txt" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzenai_onnx_utils.dll" .
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .

Download Models from HuggingFace
================================

Download the desired models from the list of pre-optimized models on Hugging Face:

.. code-block:: 
    
     # Make sure you have git-lfs installed (https://git-lfs.com) 
     git lfs install  
     git clone <link to hf model> 

For example, for Llama-2-7b-chat:

.. code-block:: 

     git lfs install  
     git clone https://huggingface.co/amd/Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid


Enabling Performance Mode (Optional)
====================================

To run the LLMs in the best performance mode, follow these steps:

- Go to ``Windows`` → ``Settings`` → ``System`` → ``Power`` and set the power mode to Best Performance.
- Execute the following commands in the terminal:

.. code-block::

   cd C:\Windows\System32\AMD
   xrt-smi configure --pmode performance


Sample C++ Program 
==================

The ``model_benchmark.exe`` test application provides a simple mechanism for running and evaluating Hybrid OGA models using the native OGA C++ APIs. The source code for this application can be used a reference implementation for how to integrate LLMs using the native OGA C++ APIs.
 
The ``model_benchmark.exe`` test application can be used as follows:

.. code-block::

     # To see available options and default settings
     .\model_benchmark.exe -h

     # To run with default settings
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths
 
     # To show more informational output
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file --verbose

     # To run with given number of generated tokens
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths -g $num_tokens

     # To run with given number of warmup iterations
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths -w $num_warmup

     # To run with given number of iterations
     .\model_benchmark.exe -i $path_to_model_dir  -f $prompt_file -l $list_of_prompt_lengths -r $num_iterations


For example, for Llama-2-7b-chat:

.. code-block::
  
     .\model_benchmark.exe -i Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid -f amd_genai_prompt.txt -l "1024" --verbose

|

**NOTE**: The C++ source code for the ``model_benchmark.exe`` executable can be found in the ``%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\c`` folder. This source code can be modified and recompiled if necessary using the commands below.

.. code-block::
  
     :: Copy project files
     xcopy /E /I "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\c" .\sources

     :: Build project
     cd sources
     cmake -G "Visual Studio 17 2022" -A x64 -S . -B build
     cmake --build build --config Release

     :: Copy runtime DLLs
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnxruntime-genai.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\onnx_custom_ops.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzen_mm.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\ryzenai_onnx_utils.dll" .\build\Release
     xcopy /Y "%RYZEN_AI_INSTALLATION_PATH%\deployment\DirectML.dll" .\build\Release

The compiled ``model_benchmark.exe`` and ``run_llm.exe`` will be saved in ``sources\build\Release``.


Sample Python Scripts
=====================

To run LLMs use the following command:

.. code-block:: 

     #To see available options and default setting:
     python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\run_model.py" -h
     #sample command
     python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\run_model.py" -m <model_folder> -l <max_token to be generated including prompt>

For example, for Llama-2-7b-chat:

.. code-block:: 

    python "%RYZEN_AI_INSTALLATION_PATH%\hybrid-llm\examples\python\run_model.py" -m "Llama-2-7b-chat-hf-awq-g128-int4-asym-fp16-onnx-hybrid" -l 128


****************
LLM Config Files
****************

Each OGA model folder contains a ``genai_config.json`` file. This file contains various configuration settings for the model. The ``session_option`` section is where information about specific runtime dependencies is specified. Within this section, the ``custom_ops_library`` option sets the path to the ``onnxruntime_vitis_ai_custom_ops.dll`` file. 

The sample below shows the defaults for the AMD pre-optimized Hybrid OGA LLMs:

.. code-block:: json

       "session_options": {
           "log_id": "onnxruntime-genai",
           "custom_ops_library": "onnx_custom_ops.dll",
           ...


The paths is relative to the folder where the program is run from. The model will error out if the ``onnxruntime_vitis_ai_custom_ops.dll`` file cannot be found at the specified location. Replacing the relative path with an absolute path to this file allows running the program from any location.


***********************
Using Fine-Tuned Models
***********************

It is also possible to run fine-tuned versions of the pre-optimized OGA models. 

To do this, the fine-tuned models must first be prepared for execution with the OGA Hybrid flow. For instructions on how to do this, refer to the page about :doc:`oga_model_prepare`.

Once a fine-tuned model has been prepared for Hybrid execution, it can be deployed by following the steps described above in this page.
